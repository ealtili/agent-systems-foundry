from pydantic import BaseModel, ConfigDict, Field


class UsageRow(BaseModel):
    """One call's token usage, flattened from the API `usage` object.

    `input_tokens` is the UNCACHED remainder only. Total prompt size is
    input_tokens + cache_read_input_tokens + both cache-creation fields.
    """

    model_config = ConfigDict(extra="forbid")

    input_tokens: int = Field(..., ge=0)
    output_tokens: int = Field(..., ge=0)
    cache_creation_5m_tokens: int = Field(default=0, ge=0)
    cache_creation_1h_tokens: int = Field(default=0, ge=0)
    cache_read_input_tokens: int = Field(default=0, ge=0)

    @property
    def prompt_tokens(self) -> int:
        return (
            self.input_tokens
            + self.cache_read_input_tokens
            + self.cache_creation_5m_tokens
            + self.cache_creation_1h_tokens
        )
