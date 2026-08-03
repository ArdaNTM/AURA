from aura.research.models import ResearchResult
from aura.research.provider import ResearchProvider


class FakeProvider(ResearchProvider):

    def search(
        self,
        query: str,
    ):
        return [
            ResearchResult(
                query=query,
                title="Test",
                content="Research data",
            )
        ]


def test_provider_contract():

    provider = FakeProvider()

    result = provider.search(
        "AURA",
    )

    assert result[0].content == "Research data"
