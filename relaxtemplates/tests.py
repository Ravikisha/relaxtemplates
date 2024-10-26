import unittest
from base import TemplateEngine


class EachTests(unittest.TestCase):

    def test_each_iterable_in_context(self):
        rendered = TemplateEngine('{% each items %}<div>{{it}}</div>{% end %}').render(items=['alex', 'maria'])
        self.assertEqual(rendered, '<div>alex</div><div>maria</div>')

    def test_each_iterable_as_literal_list(self):
        rendered = TemplateEngine('{% each [1, 2, 3] %}<div>{{it}}</div>{% end %}').render()
        self.assertEqual(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_each_parent_context(self):
        rendered = TemplateEngine('{% each [1, 2, 3] %}<div>{{..name}}-{{it}}</div>{% end %}').render(name='jon doe')
        self.assertEqual(rendered, '<div>jon doe-1</div><div>jon doe-2</div><div>jon doe-3</div>')

    def test_each_space_issues(self):
        rendered = TemplateEngine('{% each [1,2, 3]%}<div>{{it}}</div>{%end%}').render()
        self.assertEqual(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_each_no_tags_inside(self):
        rendered = TemplateEngine('{% each [1,2,3] %}<br>{% end %}').render()
        self.assertEqual(rendered, '<br><br><br>')

    def test_nested_objects(self):
        context = {'lines': [{'name': 'l1'}], 'name': 'p1'}
        rendered = TemplateEngine('<h1>{{name}}</h1>{% each lines %}<span class="{{..name}}-{{it.name}}">{{it.name}}</span>{% end %}').render(**context)
        self.assertEqual(rendered, '<h1>p1</h1><span class="p1-l1">l1</span>')

    def test_nested_tag(self):
        rendered = TemplateEngine('{% each items %}{% if it %}yes{% end %}{% end %}').render(items=['', None, '2'])
        self.assertEqual(rendered, 'yes')


class IfTests(unittest.TestCase):

    def test_simple_if_is_true(self):
        rendered = TemplateEngine('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=6)
        self.assertEqual(rendered, '<div>more than 5</div>')

    def test_simple_if_is_false(self):
        rendered = TemplateEngine('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=4)
        self.assertEqual(rendered, '')

    def test_if_else_if_branch(self):
        rendered = TemplateEngine('{% if num > 5 %}<div>more than 5</div>{% else %}<div>less than 5</div>{% end %}').render(num=6)
        self.assertEqual(rendered, '<div>more than 5</div>')

    def test_if_else_else_branch(self):
        rendered = TemplateEngine('{% if num > 5 %}<div>more than 5</div>{% else %}<div>less or equal to 5</div>{% end %}').render(num=4)
        self.assertEqual(rendered, '<div>less or equal to 5</div>')

    def test_nested_if(self):
        tmpl = '{% if num > 5 %}{% each [1, 2] %}{{it}}{% end %}{% else %}{% each [3, 4] %}{{it}}{% end %}{% end %}'
        rendered = TemplateEngine(tmpl).render(num=6)
        self.assertEqual(rendered, '12')
        rendered = TemplateEngine(tmpl).render(num=4)
        self.assertEqual(rendered, '34')

    def test_truthy_thingy(self):
        rendered = TemplateEngine('{% if items %}we have items{% end %}').render(items=[])
        self.assertEqual(rendered, '')
        rendered = TemplateEngine('{% if items %}we have items{% end %}').render(items=None)
        self.assertEqual(rendered, '')
        rendered = TemplateEngine('{% if items %}we have items{% end %}').render(items='')
        self.assertEqual(rendered, '')
        rendered = TemplateEngine('{% if items %}we have items{% end %}').render(items=[1])
        self.assertEqual(rendered, 'we have items')


def pow(m=2, e=2):
    return m ** e


class CallTests(unittest.TestCase):

    def test_no_args(self):
        rendered = TemplateEngine('{% call pow %}').render(pow=pow)
        self.assertEqual(rendered, '4')

    def test_positional_args(self):
        rendered = TemplateEngine('{% call pow 3 %}').render(pow=pow)
        self.assertEqual(rendered, '9')
        rendered = TemplateEngine('{% call pow 2 3 %}').render(pow=pow)
        self.assertEqual(rendered, '8')

    def test_keyword_args(self):
        rendered = TemplateEngine('{% call pow 2 e=5 %}').render(pow=pow)
        self.assertEqual(rendered, '32')
        rendered = TemplateEngine('{% call pow e=4 %}').render(pow=pow)
        self.assertEqual(rendered, '16')
        rendered = TemplateEngine('{% call pow m=3 e=4 %}').render(pow=pow)
        self.assertEqual(rendered, '81')


if __name__ == '__main__':
    unittest.main()