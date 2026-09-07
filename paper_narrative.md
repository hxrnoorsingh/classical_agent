# Paper Narrative — Modelling Investor Irrationality

This document locks the research narrative and paper architecture before drafting full prose. It reflects the project’s current evidence and preserves the inferential limits established in `advisor_methodology.md`.

## 1. Central research question

Can a psychologically motivated, path-dependent investment agent generate sector preferences that resemble professional investment advice more closely than selected mechanical benchmarks?

The project does not attempt to prove that professional advisors are irrational. Instead, it tests whether their observed sector recommendations are more consistent with a model containing behavioral mechanisms than with volatility targeting or momentum alone.

## 2. Core contribution

The paper makes three linked contributions:

1. It operationalizes selected behavioral-finance mechanisms—loss aversion, surprise, drawdown/reference dependence, and memory—inside a computational portfolio agent.
2. It compares that cognitive agent against a classical volatility-targeting benchmark and a momentum control to identify whether psychologically motivated state dependence produces distinct portfolio behavior.
3. It compares model-implied sector rankings with dated recommendations from Charles Schwab and Wells Fargo Investment Institute, using a pre-specified rank-based methodology with no look-ahead.

The contribution is therefore not “a better trading strategy.” It is a computational framework for asking whether observed professional advice is more consistent with behavioral state dependence than with selected mechanical alternatives.

## 3. Main hypothesis

**H1:** Professional sector recommendations will, on average, exhibit greater rank similarity to the cognitive agent than to the classical volatility-targeting benchmark or the primary momentum benchmark.

The final 11-sector pooled advisor results provide **qualified support** for H1:

- Cognitive mean Spearman rho: approximately 0.284
- Momentum A mean Spearman rho: approximately 0.224
- Classical mean Spearman rho: approximately -0.044
- Cognitive mean MARD: approximately 2.909
- Momentum A mean MARD: approximately 3.159
- Classical mean MARD: approximately 3.852

However, the result is heterogeneous across institutions. Cognitive is the stronger primary-model match for Schwab, while Momentum A marginally leads for Wells Fargo. The paper must therefore avoid presenting the cognitive advantage as universal.

## 4. Paper story in one sentence

A path-dependent agent built from behavioral-finance mechanisms produces distinct investment behavior and, across the pooled advisor sample, more closely resembles professional sector recommendations than volatility targeting or continuous momentum, although this relationship varies by institution.

## 5. Recommended paper structure

### 1. Introduction

Purpose: motivate the problem and state the research question.

The introduction should move through four ideas:

1. Standard financial models commonly summarize risk through market statistics such as volatility and drawdown, but investor decisions may also depend on psychological state and the path through which outcomes were experienced.
2. Behavioral finance identifies mechanisms such as loss aversion, reference dependence, reactions to surprise, and persistence of prior experiences.
3. This project converts those mechanisms into a stylized computational investment agent and compares it with mechanical alternatives.
4. The resulting model-generated sector preferences are then compared with dated professional sector recommendations from Schwab and Wells Fargo.

End the introduction with the research question, H1, a short methods preview, and a restrained results preview.

Suggested final-introduction result statement:

> Across the eight advisor snapshots, the cognitive agent exhibits the highest pooled rank similarity and lowest mean rank distance among the three primary models, although the result is stronger for Schwab than for Wells Fargo.

Do not open the paper by claiming that advisors are irrational.

### 2. Behavioral Motivation and Model Design

Purpose: explain what “irrationality” means operationally in this project.

This section should distinguish the three models.

#### 2.1 Classical agent

Describe the volatility-targeting model as a mechanical risk-management benchmark. It reacts to realized volatility and has no persistent psychological state.

Avoid calling it a complete “rational investor.”

#### 2.2 Cognitive agent

Explain the perceived-risk state as a combination of:

- loss sensitivity / loss aversion;
- surprise or shock relative to recent experience;
- drawdown relative to a running reference point / prior peak;
- decaying memory of prior losses.

Emphasize path dependence: two identical current market conditions can generate different cognitive exposures if the preceding histories differ.

#### 2.3 Momentum control

Explain the 12–2 momentum agent as an alternative mechanism that can also create dynamic sector preference. Its role is to prevent the paper from attributing any dynamic behavior automatically to psychology.

Momentum A is the primary continuous benchmark; Momentum B is a robustness check.

### 3. Data and Empirical Design

Purpose: make the experiment reproducible and separate model evaluation from advisor comparison.

#### 3.1 Market data

Describe SPY and the 11 U.S. sector ETFs. Note that older sector funds are date-aligned where appropriate and newer funds retain later inception dates.

#### 3.2 Computational evaluation

Describe the outputs generated from the three agents:

- Sharpe ratio;
- maximum drawdown;
- cognitive baseline stress;
- stress volatility;
- peak stress;
- stress-episode duration;
- component shares;
- ablation results;
- cognitive-momentum contamination diagnostics;
- sector stance rankings.

#### 3.3 Professional-advisor dataset

Describe the two-institution case-study design:

- Charles Schwab: four dated sector outlooks;
- Wells Fargo Investment Institute: four dated sector outlooks;
- 11 sectors per snapshot;
- 88 institution-date-sector observations total.

Explain the frozen qualitative-to-ordinal mapping and preservation of raw labels.

#### 3.4 Date alignment and no look-ahead

This deserves its own subsection because it is central to validity.

For every advisor publication date, reconstruct cognitive, classical, Momentum A, and Momentum B rankings using only market information available on or before that date.

#### 3.5 Comparison statistics

Primary statistic:

- Spearman rank correlation.

Secondary statistics:

- mean absolute rank distance (MARD);
- top-three agreement;
- bottom-three agreement.

Mention average ranks for ties and the minimum-sector rule.

### 4. Computational Results

Purpose: establish what the cognitive model actually does before comparing it with humans.

#### 4.1 Financial performance

Show that the cognitive agent does not systematically dominate on conventional performance measures. For example, SPY Sharpe is higher under the classical agent than under the cognitive agent.

Interpretation: the contribution is not superior returns; it is different risk perception and behavior.

#### 4.2 Cognitive welfare / stress ordering

Present the sector-level cognitive stress results. Highlight that sectors such as Technology, Financials, and Energy rank relatively high in baseline perceived stress, while defensive sectors are generally lower.

#### 4.3 What drives cognitive risk?

Present component shares and ablations.

The key finding is that drawdown dominates perceived risk, accounting for roughly 62%–76% of average perceived risk across sectors. Memory is the second-largest contributor. Removing drawdown causes the largest reduction in mean stress and the largest change in sector ranking.

Interpretation: empirically, the current cognitive specification behaves primarily as a reference-dependent drawdown-sensitive model with memory layered on top.

#### 4.4 Is cognitive behavior just momentum?

Present the cognitive-versus-momentum exposure correlations and R-squared values.

Explain that the relationship is material but incomplete; momentum explains only part of cognitive exposure variation. Use striking sector-ranking disagreements where useful.

### 5. Advisor Comparison Results

Purpose: test H1 directly.

#### 5.1 Pooled results

Headline primary table:

| Model | Mean Spearman rho | Mean MARD |
|---|---:|---:|
| Cognitive | ~0.284 | ~2.909 |
| Momentum A | ~0.224 | ~3.159 |
| Classical | ~-0.044 | ~3.852 |

Interpretation:

- cognitive is the closest pooled primary-model match;
- classical performs poorly as an explanation of advisor sector ordering;
- momentum remains a serious competing explanation rather than a straw-man control.

This constitutes qualified support for H1.

#### 5.2 Institution heterogeneity

Report Schwab and Wells Fargo separately.

Schwab:

- Cognitive mean rho ~0.333; MARD ~2.795
- Momentum A mean rho ~0.196; MARD ~3.386
- Classical mean rho ~0.027; MARD ~3.773

Wells Fargo:

- Cognitive mean rho ~0.235; MARD ~3.023
- Momentum A mean rho ~0.251; MARD ~2.932
- Classical mean rho ~-0.114; MARD ~3.932

Interpretation:

The pooled cognitive advantage is driven more strongly by Schwab. Wells Fargo is slightly more consistent with momentum. Therefore professional advice should not be treated as behaviorally homogeneous.

#### 5.3 Momentum B robustness

Explain that Momentum B’s rank correlation is undefined in several snapshots because binary exposures become constant across sectors. This validates its status as a secondary robustness check rather than the main competing model.

### 6. Discussion

Purpose: explain what the results mean and what they do not mean.

Organize discussion around four claims.

#### 6.1 Behavioral consistency rather than proof of irrationality

The advisor comparison shows similarity to a behavioral model, not direct evidence of advisors’ mental states.

Professional sector recommendations can also reflect valuation, macroeconomic forecasts, fundamentals, mandates, or other information absent from the computational models.

#### 6.2 Reference dependence appears especially important

Because drawdown dominates the cognitive state and its removal changes the model most strongly, the evidence is more specifically consistent with a reference-dependent / drawdown-sensitive mechanism than with an equally weighted combination of four psychological channels.

#### 6.3 Momentum remains an important competing explanation

The Wells Fargo result and pooled proximity of Momentum A make clear that trend-following information can generate recommendations that look behaviorally similar. The paper should therefore present the cognitive model as adding explanatory structure, not as uniquely identifying psychology.

#### 6.4 What the model contributes conceptually

A conventional risk-management model maps prices into exposure. The cognitive model maps prices into an internal state and then into exposure. That additional state variable allows the project to study both financial outcomes and a model-implied experience of risk.

### 7. Limitations

This section should be explicit rather than defensive.

Include:

1. The cognitive-agent parameters are stylized rather than estimated from human subjects.
2. The perceived-risk / stress variable is model-implied and is not a validated psychological welfare measure.
3. The professional-advisor sample contains only two institutions and eight snapshots.
4. Advisor recommendations may reflect information outside the model.
5. The cognitive model is dominated empirically by drawdown, so the four behavioral channels do not contribute equally.
6. Sector recommendations are ordinal and contain ties, reducing statistical resolution.
7. Momentum and cognitive behavior overlap partially, complicating causal interpretation.
8. The project tests similarity, not causality.

### 8. Conclusion

The conclusion should make three points:

1. A computational behavioral state can generate portfolio behavior that differs materially from volatility targeting.
2. The cognitive model is mainly driven by reference dependence/drawdown and is related to, but not reducible to, momentum.
3. In the two-institution advisor case study, the cognitive model provides the strongest pooled match to professional sector rankings, but the result varies across institutions and therefore supports behavioral consistency rather than a universal claim of advisor irrationality.

End with a forward-looking extension such as estimating cognitive parameters from human decision data, expanding the advisor panel, or testing whether behavioral-model similarity changes during periods of market stress.

## 6. Figure and table order

Recommended order for the final paper:

### Figures

**Figure 1 — Exposure dynamics / path dependence**
Use the existing exposure figure to visually establish how the agents respond differently through a market episode.

**Figure 2 — Cognitive risk component decomposition**
Use the existing component figure to show drawdown dominance.

**Figure 3 — Welfare / stress comparison**
Use the existing welfare figure to establish the cognitive model’s additional internal-state output.

**Figure 4 — Advisor-model similarity**
Create a new simple comparison figure showing mean Spearman rho for Cognitive, Classical, and Momentum A, preferably with Schwab and Wells Fargo distinguished.

### Tables

**Table 1 — Financial and cognitive metrics across SPY + sectors**
Existing `table1.csv`.

**Table 2 — Cognitive component shares and ablation diagnostics**
Can combine or summarize `component_shares.csv` and `ablations.csv`.

**Table 3 — Advisor-model comparison by snapshot or institution**
Primary paper table built from the final advisor comparison outputs.

A full eight-snapshot table can be moved to an appendix if space is limited.

## 7. Claims hierarchy

### Strong claims supported by the current evidence

- The cognitive agent produces path-dependent behavior that is structurally different from the classical volatility-targeting agent.
- Drawdown is the dominant component of the current cognitive perceived-risk specification.
- Cognitive exposure is related to, but not fully explained by, momentum.
- In the pooled two-institution advisor sample, cognitive rankings are closer to observed recommendations than the two primary benchmark rankings under the pre-specified comparison metrics.
- The advisor result is heterogeneous across Schwab and Wells Fargo.

### Claims that require cautious wording

- Professional advice may contain behavioral influences.
- Reference dependence may help explain some professional recommendations.
- Cognitive modelling may capture dimensions of advisor behavior that volatility targeting omits.

### Claims the paper should not make

- Schwab or Wells Fargo is irrational.
- Professional advisors generally are irrational.
- The cognitive agent identifies the true psychological process used by advisors.
- The cognitive model is validated as a measure of human welfare.
- The cognitive strategy is financially superior.
- The results establish causality.

## 8. Abstract logic to use later

When drafting the abstract, use this order:

1. Problem: conventional portfolio rules omit psychological state.
2. Method: build cognitive, classical, and momentum agents on U.S. sector returns.
3. Mechanism: cognitive risk uses losses, shocks, drawdown, and memory.
4. Validation/control: compare behavior, components, ablations, and momentum contamination.
5. Human comparison: eight dated sector outlooks from Schwab and Wells Fargo, 88 advisor-sector observations, no look-ahead.
6. Main result: cognitive leads pooled primary-model similarity but not uniformly across institutions.
7. Interpretation: evidence is consistent with behavioral influences but does not establish advisor irrationality.

## 9. Symposium presentation narrative

For the oral presentation, compress the entire project into this sequence:

1. **Question:** Can we model investor irrationality rather than just describe it?
2. **Model:** Build a cognitive investor with loss aversion, surprise, drawdown, and memory.
3. **Benchmarks:** Compare against volatility targeting and momentum.
4. **Mechanism result:** Cognitive risk is mainly driven by drawdown/reference dependence.
5. **Human test:** Compare dated model sector rankings with Schwab and Wells Fargo recommendations.
6. **Finding:** Cognitive is the best pooled match, especially for Schwab; Wells Fargo is slightly more momentum-like.
7. **Conclusion:** Professional advice sometimes resembles a path-dependent behavioral model more than a mechanical risk model, but the evidence is heterogeneous and does not prove irrationality.

## 10. Next writing task

With the narrative locked, the next task should be **Task #4: build the literature/references framework and then draft the Introduction + Behavioral Motivation sections**. The literature stage should happen before final prose so theoretical claims about loss aversion, reference dependence, memory, and momentum are properly grounded rather than retrofitted after writing.
