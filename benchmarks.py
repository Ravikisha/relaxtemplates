import os
import timeit
from jinja2 import Environment, FileSystemLoader, Template as JinjaTemplate
from django.conf import settings
from django.template import Context, Template as DjangoTemplate
from django.template.loader import get_template
from django import setup as django_setup
from relaxtemplates import TemplateEngine as MicroTemplate

# Define the template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# Context to be used in all templates
context = {
    'title': 'MY TODOS',
    'todos': [
        dict(title='grocery shopping', description='do all the shopping', done=True, followers=[]),
        dict(title='pay bills', description='pay all the bills', done=False, followers=['alex']),
        dict(title='go clubbing', description='get drunk', done=False, followers=['alex', 'mike', 'paul']),
    ]
}

# Django settings configuration
if not settings.configured:
    settings.configure(
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [template_dir],
                'APP_DIRS': True,
            }
        ]
    )
    django_setup()  # This initializes the Django environment.

def read_html(engine):
    """Reads the HTML template file for the given engine."""
    html_file_path = os.path.join(template_dir, f"{engine}.html")
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"Template file {html_file_path} does not exist.")
    with open(html_file_path) as html_file:
        html = html_file.read()
    return html

# Read template contents for each engine
relaxtemplates_html = read_html('relaxtemplates')
django_html = read_html('django')
jinja2_html = read_html('jinja2')
jinja2_env = Environment(loader=FileSystemLoader(template_dir))


# Benchmark functions for each engine
def benchmark_relaxtemplates():
    MicroTemplate(relaxtemplates_html).render(**context)

def benchmark_django():
    DjangoTemplate(django_html).render(Context(context))


def benchmark_django_default_loader():
    template = get_template('django.html')
    template.render(context)


def benchmark_jinja2():
    JinjaTemplate(jinja2_html).render(**context)


def benchmark_jinja2_env():
    jinja2_env.get_template('jinja2.html').render(**context)


# Benchmark execution
if __name__ == '__main__':
    number = 10000
    engines = ('relaxtemplates',  'django', 'django_default_loader','jinja2',  'jinja2_env')
    setup = "from __main__ import %s" % ', '.join(map(lambda t: 'benchmark_' + t, engines))
    
    for engine in engines:
        t = timeit.Timer(f"benchmark_{engine}()", setup=setup)
        time = t.timeit(number=number) / number
        print(f"{engine} => run {number} times, took {1000 * time:.2f} ms")
