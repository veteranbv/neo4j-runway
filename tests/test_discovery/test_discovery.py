from io import StringIO
import unittest
import sys

import pandas as pd

from neo4j_runway.discovery.discovery import Discovery
from neo4j_runway.llm.llm import LLM
from neo4j_runway.models import UserInput

USER_GENERATED_INPUT = {
    "general_description": "This is data on some interesting data.",
    "id": "unique id for a node.",
    "feature_1": "this is a feature",
    "feature_2": "this is also a feature",
}

data = {
    "id": [1, 2, 3, 4, 5],
    "feature_1": ["a", "b", "c", "d", "e"],
    "feature_2": ["z", "y", "x", "w", "v"],
    "bad_feature": [11, 22, 33, 44, 55],
}


class TestDiscovery(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.disc = Discovery(
            llm=LLM(), user_input=USER_GENERATED_INPUT, data=pd.DataFrame(data)
        )

    def test_initialized_variables(self) -> None:
        """
        Ensure that all initial variables are set accurately.
        """

        self.assertEqual(self.disc.discovery, "")
        self.assertEqual(
            set(self.disc.columns_of_interest), {"id", "feature_1", "feature_2"}
        )
        self.assertEqual(set(self.disc.data.columns), {"id", "feature_1", "feature_2"})

    def test_init_with_UserInput(self) -> None:
        user_input = UserInput(
            general_description="This is a general description.",
            column_descriptions={"feature_1": "column one", "feature_2": " column two"},
        )

        self.test_disc = Discovery(
            llm=LLM(), user_input=user_input, data=pd.DataFrame(data)
        )

        self.assertEqual(self.test_disc.discovery, "")
        self.assertEqual(
            set(self.test_disc.columns_of_interest), {"feature_1", "feature_2"}
        )
        self.assertEqual(set(self.test_disc.data.columns), {"feature_1", "feature_2"})

    def test_init_with_no_desired_columns(self) -> None:
        d = Discovery(llm=LLM(), data=pd.DataFrame(data))

        self.assertEqual(
            {"id", "feature_1", "feature_2", "bad_feature"}, set(d.columns_of_interest)
        )

        with self.assertWarns(Warning):
            Discovery(llm=LLM(), data=pd.DataFrame(data))

    def test_view_discovery_no_notebook(self) -> None:
        d = Discovery(data=pd.DataFrame(data))
        test_disc = "TEST\ntest"
        d.discovery = test_disc

        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        d.view_discovery(notebook=False)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), test_disc + "\n")

    def test_view_discovery_with_notebook(self) -> None:
        d = Discovery(data=pd.DataFrame(data))
        test_disc = "TEST\ntest"
        d.discovery = test_disc

        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        d.view_discovery(notebook=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(
            capturedOutput.getvalue().strip(), "<IPython.core.display.Markdown object>"
        )


if __name__ == "__main__":
    unittest.main()
