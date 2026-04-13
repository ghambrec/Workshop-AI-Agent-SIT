from typing import Dict, Any

from deepeval.metrics import ToolCorrectnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, ToolCall
from langfuse import Evaluation

from app.evaluation.providers import VertexGemini


## LLM-based evaluation
async def answer_relevancy(
    input: Dict[str, Any],
    output: Dict[str, Any],
    expected_output: str,
    metadata: Dict[str, Any] | None,
    **kwargs,
):
    # trace= langfuse.api.trace.get(langfuse.get_current_trace_id())
    # 1. Get all observations for the trace
    # The 'get_many' method allows filtering by trace_id
    metric = AnswerRelevancyMetric(
        threshold=0.7, model=VertexGemini(), include_reason=True
    )

    test_case = LLMTestCase(
        input=input["question"],
        actual_output=output["output"],
        expected_output=expected_output,
    )

    res = await metric.a_measure(test_case)

    return Evaluation(name="answer_relevancy", value=res, comment="Glean..")


## Trajectory-based metric..
async def tool_calling_accuracy(
    input: Dict[str, Any],
    output: Dict[str, Any],
    expected_output: str,
    metadata: Dict[str, Any] | None,
    **kwargs,
):

    def convert_to_tool_calls(calls: list[str]) -> list[ToolCall]:
        return [ToolCall(name=call, input_parameters=None) for call in calls]

    tool_calls_list = [
        ToolCall(name=call.tool_name, input_parameters=None)
        for call in output["eval_metadata"]["tool_calls"]
    ]
    metric = ToolCorrectnessMetric(model=VertexGemini())

    # convert to tool calls...
    test_case = LLMTestCase(
        input=input["question"],
        actual_output=output["output"],
        expected_output=expected_output,
        tools_called=tool_calls_list,
        expected_tools=convert_to_tool_calls(metadata["expected_tool_calls"]),
    )

    res = await metric.a_measure(test_case)
    return Evaluation(name="tool_call_accuracy", value=res)
