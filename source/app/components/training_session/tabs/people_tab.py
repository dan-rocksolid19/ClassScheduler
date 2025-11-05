from librepy.app.components.settings.tabs.base_tab import BaseTab


class PeopleTab(BaseTab):
    """Empty People tab for future use."""

    def build(self):
        # For now, add a placeholder label
        self.dialog.add_label(
            'LblPeoplePlaceholder',
            20,
            20,
            300,
            16,
            Label='No people to configure yet.',
            page=self.page,
            FontWeight=100,
            FontHeight=10,
        )

    def commit(self) -> dict:
        # Nothing to contribute yet
        return {}
