# Optimization Summary

The v2 dataset, the four evaluators, the prompt and the temperature were held constant while the system under test was switched from `gpt-4o-mini` to `gpt-4o`. `gpt-4o` scored 15 out of 15 on all four evaluators, resolving the one letter the smaller model had missed. The cost of that improvement was roughly sixteen times per run, 0.01155 USD against 0.00069 USD for the same 15 examples, with no meaningful latency difference. On the evidence gathered, the two models were indistinguishable on 14 of 15 examples, and a one example difference at n=15 is not sufficient to conclude that either model is better at this task.

## Comparison

| Evaluator | gpt-4o-mini | gpt-4o |
|---|---|---|
| reason_code_exact | 14/15 | 15/15 |
| manual_review_exact | 15/15 | 15/15 |
| correctness (OpenAI judge) | 14/15 | 15/15 |
| deepseek_correctness (DeepSeek judge) | 14/15 | 15/15 |
| Run cost, 15 examples | 0.00069 USD | 0.01155 USD |
| Mean latency | 0.96 s | 0.99 s |

## Reading the result

The finding that carries weight here is the cost ratio, not the score difference. Paying approximately sixteen times more per call to resolve a single ambiguous example would be poor value in most production settings, particularly since the failing letter was one deliberately written to withhold the decisive detail. A deployment choice made on this evidence would favour `gpt-4o-mini`, with the harder cases routed to human handling rather than to a larger model.

The comparison is also limited by the same ceiling problem that affected the dataset itself. With `gpt-4o` at 15 out of 15, the dataset cannot distinguish it from any model that also scores 15 out of 15, so no upper bound on its capability has been established. A larger and harder dataset would be needed before either model could be recommended on measured grounds.

An untested alternative is prompt revision rather than model substitution. The failing letter turned on recognising an unnamed credit reference agency, which a prompt naming the common agencies might have handled at the smaller model's cost. That was not attempted here.
