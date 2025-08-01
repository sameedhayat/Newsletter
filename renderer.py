import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

class Renderer:
    """
    Renders newsletter content into Markdown or HTML using Jinja2 templates.
    """
    def __init__(self, template_dir: str = "templates"):
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        # Load templates
        self.md_template  = self.env.get_template('newsletter.md.j2')
        self.html_template = self.env.get_template('newsletter.html.j2')

    def render_markdown(self, data: dict, summary: str) -> str:
        """
        Render the newsletter as Markdown.
        :param data: dictionary with keys 'articles', 'papers', 'repos'
        :param summary: overview summary string
        :return: rendered Markdown string
        """
        return self.md_template.render(data=data, summary=summary)

    def render_html(self, data: dict, summary: str) -> str:
        """
        Render the newsletter as HTML.
        :param data: dictionary with keys 'articles', 'papers', 'repos'
        :param summary: overview summary string
        :return: rendered HTML string
        """
        return self.html_template.render(data=data, summary=summary)
