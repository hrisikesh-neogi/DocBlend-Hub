from typing import Any, Dict, List, Optional
from pydantic import Extra, root_validator, validator
from langchain.prompts.base import StringPromptTemplate,DEFAULT_FORMATTER_MAPPING
from pydantic import BaseModel


class VideoSummarizerPromptTemplate(StringPromptTemplate, BaseModel):
    """prompt template that contains video summarization prompts"""
    prefix: str = None
    suffix: str = None
    input_variables: list = None
    template_format: str = "f-string"



    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        if len(v) ==0 or "text" not in v:
            raise ValueError("text must be the only input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # Get the source code of the function

        kwargs = self._merge_partial_and_user_variables(**kwargs)
        pieces = [self.prefix, self.suffix]

        for input_variable in self.input_variables:
            if not input_variable in kwargs.keys():
                raise ValueError(f"Input variables does not match with the parameters. \n{input_variable}")


        # Generate the prompt to be sent to the language model
        template = "\n".join(
            [piece for piece in pieces if piece]
        )
        return DEFAULT_FORMATTER_MAPPING[self.template_format](template, **kwargs)

    def _prompt_type(self):
        return "function-explainer"

