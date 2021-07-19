import abc
from collections import defaultdict, Counter

from requests.api import delete
from eval import EvalRecord, Textline
from config import LANG_CONFIG, ENTITY_UNION_CONFIG, DOC_TYPED_SEGMENTS

from tqdm.auto import tqdm
from tabulate import tabulate


class TextlineTagger(abc.ABC):
    @abc.abstractmethod
    def tag_line(self, textline: Textline) -> list:
        pass

    @property
    def name(self):
        return self.__class__.__name__


class TextlineCollection(dict):
    def add_textline(self, textline, tag_list):
        if tag_list is None:
            return
        for tag in tag_list:
            if tag not in self:
                self[tag] = []

            self[tag].append(textline)

    @property
    def tags(self):
        return self.keys()

    @property
    def textline_count(self):
        return sum(len(textline_list) for textline_list in self.values())

    @property
    def unique_textline_count(self):
        textline_set = set([
            line['textline_id'] for textline_list in self.values()
            for line in textline_list
        ])
        return len(textline_set)

    @property
    def distribution(self):
        dist = {}
        for tag in self:
            count = len(self[tag])
            percent = round((count / self.textline_count) * 100, 2)
            dist[tag] = {'count': count, 'percentage': percent}
        return dist

    @property
    def image_stats(self):
        counts_by_tag = {}
        for tag in self:
            counter = Counter([line.idx.split('.')[0] for line in self[tag]])
            counts_by_tag[tag] = counter

        tag_counts_by_image_id = defaultdict(dict)
        for tag, counts in counts_by_tag.items():
            for imageid, cnt in counts.items():
                tag_counts_by_image_id[imageid][tag] = cnt

        return tag_counts_by_image_id

    def get_image_list_of_tag(self, tag):
        return Counter([line.idx.split('.')[0] for line in self[tag]])


class EvalAnalyzer:
    def __init__(self):
        self.taggers = []

    def register_textline_tagger(self, tagger):
        self.taggers.append(tagger)

    def analyze_one_record(self,
                           record_id,
                           script,
                           doc_only,
                           entity=None,
                           lvl=None):
        textlines = {
            tagger.name: TextlineCollection()
            for tagger in self.taggers
        }
        for textline in tqdm(
                self._iter_textlines(record_id, script, doc_only, entity,
                                     lvl)):
            for tagger in self.taggers:
                textlines[tagger.name].add_textline(textline,
                                                    tagger.tag_line(textline))

        return textlines

    def analyze(self, record_ids, script, doc_only, entity=None, lvl=None):
        analysis = []
        for alias, record_id in record_ids:
            analysis.append((alias,
                             self.analyze_one_record(record_id, script,
                                                     doc_only, entity, lvl)))
        return analysis

    @staticmethod
    def format(analysis_results, max_tag_count=10):
        _, baseline_textlines = analysis_results[0]
        formatted_per_tagger = {}
        for tagger_name, textline_collection in baseline_textlines.items():
            compare_result = {}
            distribution = textline_collection.distribution
            for tag, data in sorted(distribution.items(),
                                    key=lambda dist: dist[1]['count'],
                                    reverse=True)[:max_tag_count]:
                comp = {}

                for metric, value in data.items():
                    comp[metric] = {'values': [value], 'diff': []}
                    for alias, result in analysis_results[1:]:
                        cur_data = result[tagger_name].distribution.get(
                            tag, {})
                        cur_value = cur_data.get(metric, 0)
                        comp[metric]['values'].append(cur_value)
                        comp[metric]['diff'].append(cur_value - value)
                compare_result[tag] = comp
            if len(analysis_results) > 1:
                sorted_result = sorted(
                    compare_result.items(),
                    key=lambda record: record[1]['count']['diff'][-1],
                    reverse=True)
            else:
                sorted_result = compare_result.items()
            headers = list(list(compare_result.values())[0].keys())
            print_list = []
            for tag, comp in sorted_result:
                line = [tag]
                for header in headers:
                    cur_col = comp[header]
                    line.append(cur_col['values'][0])
                    for v, d in zip(cur_col['values'][1:], cur_col['diff']):
                        cur_str = f'{v}('
                        if d > 0:
                            cur_str += '+'
                        if isinstance(d, float):
                            cur_str += f'{d:.2f})'
                        else:
                            cur_str += f'{d})'
                        line.append(cur_str)
                print_list.append(line)

            print_headers = ['key']
            for header in headers:
                for alias, _ in analysis_results:
                    print_headers.append(f'{header} {alias}')
            formatted_per_tagger[tagger_name] = tabulate(print_list,
                                                         headers=print_headers)
        return formatted_per_tagger

    @staticmethod
    def _iter_textlines(record_id, script, doc_only, entity, lvl=None):
        lang_list = LANG_CONFIG[script]
        entity_list = ENTITY_UNION_CONFIG[entity] if entity else None
        record = EvalRecord(record_id)

        for exp in record.exps:
            if not exp.language in lang_list:
                continue
            for cat in exp.categories:
                if doc_only and cat.name not in DOC_TYPED_SEGMENTS:
                    continue
                if entity_list:
                    textlines = cat.textlines_entity_metrics(lvl)
                else:
                    textlines = cat.textlines_word_metrics()
                for line in filter(
                        lambda textline: not textline.entity or textline.entity
                        in entity_list, textlines):
                    yield line
