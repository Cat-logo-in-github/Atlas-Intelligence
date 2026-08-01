from pathlib import Path

from atlas.models.metadata import Metadata


class Module:

    def __init__(
        self,
        path: Path
    ):
        self.path = path

        self.metadata = Metadata.from_file(
            path / "metadata.yaml"
        )

    @property
    def title(self):
        return self.metadata.title

    @property
    def slug(self):
        return self.metadata.slug

    @property
    def module(self):
        return self.metadata.module

    @property
    def status(self):
        return self.metadata.status

    @property
    def difficulty(self):
        return self.metadata.difficulty

    @property
    def tags(self):
        return self.metadata.tags

    @property
    def related(self):
        return self.metadata.related

    @property
    def updated(self):
        return self.metadata.updated

    @property
    def outputs(self):
        return self.metadata.outputs

    @property
    def website_enabled(self):
        return self.outputs.website.published

    @property
    def youtube_output(self):
        return self.outputs.youtube

    @property
    def youtube_enabled(self):
        return self.outputs.youtube.published

    @property
    def youtube_url(self):
        return self.outputs.youtube.url

    @property
    def blog_output(self):
        return self.outputs.blog

    @property
    def blog_enabled(self):
        return self.outputs.blog.published

    @property
    def blog_url(self):
        return self.outputs.blog.url

    @property
    def notebook_output(self):
        return self.outputs.notebook

    @property
    def notebook_enabled(self):
        return self.outputs.notebook.published

    @property
    def simulation_output(self):
        return self.outputs.simulation

    @property
    def simulation_enabled(self):
        return self.outputs.simulation.published

    @property
    def knowledge(self):
        return self.path / "knowledge.md"

    @property
    def blog(self):
        return self.path / "blog.md"

    @property
    def notebook(self):
        return self.path / "notebook.ipynb"

    @property
    def assets(self):
        return self.path / "assets"

    @property
    def simulation(self):
        return self.path / "simulation"

    @property
    def generated(self):
        return self.path / "generated"

    @classmethod
    def load_all(
        cls,
        modules_dir: Path
    ):
        modules = []

        if not modules_dir.exists():
            return modules

        for folder in modules_dir.iterdir():

            if not folder.is_dir():
                continue

            if not (folder / "metadata.yaml").exists():
                continue

            modules.append(
                cls(folder)
            )

        return modules