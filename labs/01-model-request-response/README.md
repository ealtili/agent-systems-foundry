# Lab 01: Model Request-Response & Structured Output

## Systems Context
The foundation of agent engineering is establishing a reliable contract between a stochastic language model and deterministic software. We do not evaluate "did the prompt work?"—we measure the empirical boundary characteristics of structured extraction vs. raw completions.

## Objectives
1. Implement both System A (unstructured regex extraction) and System B (Pydantic schema enforcement).
2. Measure the exact latency, token overhead, and error rate across both systems.
3. Build a resilient parsing and validation harness with recovery strategies.
4. Pass the oral architectural defense (`/defend 01`).

## Architecture
```
User Request ---> [Prompt Builder] ---> Anthropic API
                                                |
                                        Raw Output JSON
                                                |
                                      [Pydantic Validator]
                                     /                    \
                                  Success                Failure
                                     |                      |
                              Structured Payload      [Recovery Loop]
```
