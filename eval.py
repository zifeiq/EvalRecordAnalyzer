from pathlib import Path
from backend_api import get_details_of_record_id, get_eval_file, list_eval_dir


class EvalRecord:
    def __init__(self, record_id) -> None:
        self._details = get_details_of_record_id(record_id)['details']

    @property
    def exps(self):
        return [EvalExperiment(desc) for desc in self._details]


class EvalExperiment:
    def __init__(self, descriptor):
        self._desc = descriptor

    @property
    def language(self):
        return self._desc['language']

    @property
    def algo(self):
        return self._desc['algorithm']

    @property
    def datset(self):
        return self._desc['dataset']

    @property
    def categories(self):
        files = list_eval_dir(self._desc['storageRoot'])
        categories = [file for file in files if not Path(file).suffix]
        return [
            Category(Path(self._desc['storageRoot'], cat))
            for cat in categories
        ]


class Category:
    def __init__(self, root_path):
        self._root = root_path

    @property
    def name(self):
        return self._root.name

    @property
    def textlines_word_metrics(self):
        return self._make_textlines(
            get_eval_file(str(self._root / 'textline_word_metrics.json')))

    def textlines_entity_metrics(self, lvl=None):
        lvl_str = ''
        if lvl:
            lvl_str = f'_{lvl}'
        return self._make_textlines(
            get_eval_file(
                str(self._root / f'textline_entity_metrics{lvl_str}.json')))

    @staticmethod
    def _make_textlines(obj):
        return [
            Textline(obj) for textline_list in obj.values()
            for obj in textline_list
        ]


class Textline:
    def __init__(self, textline_obj):
        self._obj = textline_obj

    @property
    def is_debug_line(self):
        return 'REF' not in self._obj

    @property
    def idx(self):
        return self._obj.get('textline_id')

    @property
    def image_id(self):
        return self.idx.split('.')[0]

    @property
    def ref(self):
        return self._obj.get('REF')

    @property
    def hyp(self):
        return self._obj.get('HYP')

    @property
    def insert_err(self):
        return self._obj.get('insert_error')

    @property
    def subs_err(self):
        return self._obj.get('subs_error')

    @property
    def del_err(self):
        return self._obj.get('delete_error')

    @property
    def entity(self):
        return self._obj.get('entity_name')

    @property
    def tags(self):
        return self._obj.get('tags', '').split()

    def __str__(self):
        return f"""
id: {self.idx}
ref: {self.ref}
hyp: {self.hyp}
subs: {self.subs_err}
del: {self.del_err}
ins: {self.insert_err}
tags: {self.tags}
entity: {self.entity}"""

    def __repr__(self):
        return str(self)