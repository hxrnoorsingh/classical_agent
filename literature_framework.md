# Literature Framework — Modelling Investor Irrationality

This document maps the project's theoretical mechanisms to the academic literature that should support the paper. It is a writing guide, not the finished literature review.

## 1. Behavioral finance as the umbrella framework

### Barberis & Thaler (2003) — *A Survey of Behavioral Finance*

**Use in the paper:** opening theoretical frame.

Behavioral finance studies financial phenomena using models in which some agents are not fully rational and where psychology and limits to arbitrage matter. This is the appropriate umbrella literature for the project because the cognitive agent deliberately relaxes the assumption that portfolio decisions depend only on conventional statistical risk.

**How to use it:** cite in the Introduction when explaining why psychologically motivated decision rules can be meaningful objects of financial research.

**Source:** Handbook of the Economics of Finance, 1B, 1053–1128. DOI: `10.1016/S1574-0102(03)01027-6`.

---

## 2. Prospect theory, loss aversion, and reference dependence

### Kahneman & Tversky (1979) — *Prospect Theory: An Analysis of Decision under Risk*

**Use in the paper:** foundational citation for gains/losses being evaluated relative to a reference point and for asymmetric treatment of losses and gains.

Prospect theory challenges expected-utility descriptions of risky choice by describing decisions in terms of gains and losses relative to a reference point rather than final wealth alone. This motivates the cognitive model's asymmetric loss term and the broader idea that identical objective outcomes can be perceived differently depending on prior position.

**Important caution:** the implemented agent is inspired by prospect-theoretic ideas; it is not a literal estimation or implementation of the full prospect-theory value and probability-weighting functions.

**Source:** *Econometrica* 47(2), 263–291/292. DOI: `10.2307/1914185`.

### Tversky & Kahneman (1992) — *Advances in Prospect Theory: Cumulative Representation of Uncertainty*

**Use in the paper:** stronger modern foundation for loss aversion and reference-dependent valuation.

Cumulative prospect theory formalizes loss aversion and diminishing sensitivity and allows different treatment of gains and losses. This provides theoretical grounding for the cognitive model's stronger response to losses than to equivalent favorable outcomes.

**Source:** *Journal of Risk and Uncertainty* 5, 297–323. DOI: `10.1007/BF00122574`.

### Tversky & Kahneman (1991) — *Loss Aversion in Riskless Choice: A Reference-Dependent Model*

**Use in the paper:** optional supporting citation if the discussion emphasizes reference dependence more than risky probability weighting.

This paper develops reference-dependent preferences and loss aversion in riskless choice. It is particularly useful because the project's empirically dominant cognitive component is drawdown/reference dependence.

**Source:** *Quarterly Journal of Economics* 106(4), 1039–1061.

---

## 3. Prior outcomes, path dependence, and investor state

### Barberis, Huang & Santos (2001) — *Prospect Theory and Asset Prices*

**Use in the paper:** one of the most important sources for the project's state-dependent design.

The paper models investors who derive utility from changes in financial wealth, with loss aversion depending on prior investment performance. This is directly relevant to the project's idea that current risk tolerance can depend on the path of prior outcomes rather than only on contemporaneous volatility.

**Why it matters for this project:** it gives a finance-specific precedent for allowing prior gains and losses to alter subsequent attitudes toward risk. This is conceptually close to the cognitive agent's persistent memory and running-peak state.

**Source:** *Quarterly Journal of Economics* 116(1), 1–53. DOI: `10.1162/003355301556310`.

### Interpretation for the paper

The safest language is not that the model literally reproduces human memory. Instead write that it introduces a **stylized persistent state variable** motivated by evidence and theory that prior investment outcomes can affect subsequent risky choice.

---

## 4. Drawdown and reference-point effects

The current computational results make this literature especially important because drawdown accounts for most of the model's average perceived risk.

### Grinblatt & Han (2005) — *Prospect Theory, Mental Accounting, and Momentum*

**Use in the paper:** bridge between reference points and asset-price behavior.

The paper develops a model in which prospect theory and mental accounting generate a disposition effect and reference-price dynamics. The resulting gap between fundamental value and equilibrium price can produce return predictability and momentum.

**Why this source is unusually important:** it shows that reference-dependent behavioral mechanisms and momentum can be connected rather than mutually exclusive. Therefore the project's momentum agent is an essential competing explanation, not merely a generic control.

**Source:** *Journal of Financial Economics* 78(2), 311–339. DOI: `10.1016/j.jfineco.2004.10.006`.

### Implication for our interpretation

Because the cognitive model is empirically dominated by drawdown, the paper should describe it as primarily a **reference-dependent / drawdown-sensitive behavioral risk model with memory**, rather than suggesting that all four cognitive components contribute equally.

---

## 5. Momentum as the competing explanation

### Jegadeesh & Titman (1993) — *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency*

**Use in the paper:** foundational empirical citation for momentum.

Jegadeesh and Titman document that strategies buying recent winners and selling recent losers generate positive returns over intermediate horizons. This establishes momentum as a serious empirical regularity rather than an arbitrary benchmark chosen for this project.

**Source:** *Journal of Finance* 48(1), 65–91. DOI: `10.1111/j.1540-6261.1993.tb04702.x`.

### Why the momentum agent is necessary

A time-varying cognitive strategy may look psychologically sophisticated while simply responding to price continuation. The momentum control asks whether sector rankings that resemble professional advice can already be generated from recent trends.

The paper's logic is therefore:

- **Classical agent:** can volatility/risk management explain the ranking?
- **Momentum agent:** can trend-following explain the ranking?
- **Cognitive agent:** does a path-dependent behavioral risk state add explanatory similarity beyond those simpler mechanisms?

### Grinblatt & Han (2005) as a bridge

This citation should appear again in the momentum subsection because it demonstrates that behavioral reference dependence can itself generate momentum-like price dynamics. That makes it especially important not to interpret cognitive-versus-momentum comparisons as a clean separation between “psychology” and “non-psychology.”

---

## 6. Professional investors can exhibit behavioral patterns

### Shapira & Venezia (2001) — *Patterns of Behavior of Professionally Managed and Independent Investors*

**Use in the paper:** justification for examining professional advice rather than assuming behavioral biases apply only to retail investors.

The study compares independently managed and professionally managed brokerage accounts and reports disposition-effect behavior in both groups, although stronger among independent investors.

**How to use it:** cite carefully. It supports the proposition that professional management does not automatically eliminate all behavioral patterns. It does **not** support claiming that Schwab or Wells Fargo are irrational.

**Source:** *Journal of Banking & Finance* 25(8), 1573–1587. DOI: `10.1016/S0378-4266(00)00139-4`.

### Locke & Mann (2005) — *Professional Trader Discipline and Trade Disposition*

**Use in the paper:** counterweight and nuance.

This study investigates professional futures traders. Although loss-holding behavior is observed, successful traders can also display disciplined behavior without evidence of associated costs. This is useful because it prevents the literature review from implying that all behavioral-looking professional behavior is necessarily irrational or harmful.

**Source:** *Journal of Financial Economics* 76(2), 401–444. DOI: `10.1016/j.jfineco.2004.01.004`.

### Narrative implication

Together, Shapira–Venezia and Locke–Mann support a nuanced claim:

> Professional market participants may exhibit behavioral patterns, but expertise and discipline can reduce or alter their consequences; observing a behavioral pattern is not equivalent to proving irrationality.

That is exactly the interpretive boundary needed for the advisor comparison.

---

## 7. Computational and agent-based finance

### LeBaron (2006) — *Agent-Based Computational Finance*

**Use in the paper:** methodological precedent for studying financial behavior through computational agents.

LeBaron surveys agent-based financial models in which computational tools are used to study investor heterogeneity and market dynamics. This gives the project a broader methodological home: using explicitly programmed agents to study how different decision rules generate different financial behavior.

**Source:** in *Handbook of Computational Economics*, Vol. 2, pp. 1187–1233. DOI: `10.1016/S1574-0021(05)02024-1`.

### Arthur, Holland, LeBaron, Palmer & Tayler (1997) — *Asset Pricing Under Endogenous Expectations in an Artificial Stock Market*

**Use in the paper:** optional deeper methodological citation.

This classic artificial-market work studies heterogeneous adaptive agents whose expectations evolve within the market they collectively create. Your project is much simpler and does not simulate an endogenous market, but the paper can cite this literature as precedent for using computational agent heterogeneity to investigate financial behavior.

**Important distinction:** your agents are applied to historical return series; they do not jointly generate equilibrium prices. Do not describe the project as a full agent-based market simulation.

---

## 8. How these sources map onto the cognitive model

| Model component / paper idea | Primary literature support | What the source supports | What it does NOT prove |
|---|---|---|---|
| Loss sensitivity | Kahneman & Tversky (1979); Tversky & Kahneman (1992) | Gains and losses can be treated asymmetrically; loss aversion/reference dependence are established behavioral concepts | The project's numerical loss coefficient is empirically estimated |
| Drawdown / reference point | Tversky & Kahneman (1991, 1992); Grinblatt & Han (2005) | Evaluation relative to reference points can alter decisions and market behavior | Running portfolio peak is the uniquely correct human reference point |
| Memory / prior outcomes | Barberis, Huang & Santos (2001) | Prior investment performance can affect subsequent risk attitudes | The project's exponential decay parameter is psychologically validated |
| Momentum benchmark | Jegadeesh & Titman (1993) | Intermediate-horizon return continuation is a major empirical regularity | Momentum explains advisor reasoning |
| Behavioral–momentum overlap | Grinblatt & Han (2005) | Reference-dependent behavior can contribute to momentum-like dynamics | Cognitive and momentum mechanisms are fully separable |
| Professional behavioral patterns | Shapira & Venezia (2001); Locke & Mann (2005) | Professional investors can exhibit behavioral-looking patterns, with important nuance | Schwab/Wells Fargo sector views are caused by bias |
| Computational-agent method | LeBaron (2006); Arthur et al. (1997) | Computational heterogeneous-agent approaches are established in finance | This project is a full market-equilibrium agent-based simulation |

---

## 9. Literature-review argument for the paper

The literature section should not become a list of biases. It should build a chain of reasoning:

1. Traditional financial decision rules need not capture all observed investor behavior; behavioral finance provides models with psychologically motivated deviations from full rationality (Barberis & Thaler).
2. Prospect theory introduces reference-dependent evaluation and asymmetric sensitivity to losses (Kahneman & Tversky; Tversky & Kahneman).
3. Financial models have incorporated prior gains and losses into state-dependent risk attitudes (Barberis, Huang & Santos).
4. Reference-dependent behavior can affect trading and can even generate momentum-like patterns (Grinblatt & Han).
5. Momentum is independently well documented and therefore must be treated as a competing explanation (Jegadeesh & Titman).
6. Professional investors are not automatically free of behavioral patterns, but apparent bias should not automatically be equated with costly irrationality (Shapira & Venezia; Locke & Mann).
7. Computational-agent methods provide a natural way to compare the behavior generated by different decision rules (LeBaron).

That chain leads directly to the research question rather than retrofitting citations onto the model.

---

## 10. Suggested Introduction citation sequence

A concise Introduction can use roughly this order:

1. **Barberis & Thaler (2003)** — behavioral finance motivation.
2. **Kahneman & Tversky (1979)** and/or **Tversky & Kahneman (1992)** — loss aversion and reference dependence.
3. **Barberis, Huang & Santos (2001)** — path-dependent prior performance in asset pricing.
4. **Jegadeesh & Titman (1993)** — momentum as a competing empirical mechanism.
5. **Shapira & Venezia (2001)** — motivation for examining professionals.
6. State the gap: rather than identifying a single bias in trading records, this project constructs a stylized cognitive risk state and asks which model-generated sector ordering most resembles dated professional sector advice.

---

## 11. Recommended core bibliography

The paper does not need dozens of citations for a symposium project. A strong core bibliography would begin with these nine:

1. Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291/292.
2. Tversky, A., & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. *Journal of Risk and Uncertainty*, 5, 297–323.
3. Barberis, N., Huang, M., & Santos, T. (2001). Prospect theory and asset prices. *Quarterly Journal of Economics*, 116(1), 1–53.
4. Barberis, N., & Thaler, R. (2003). A survey of behavioral finance. *Handbook of the Economics of Finance*, 1B, 1053–1128.
5. Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers: Implications for stock market efficiency. *Journal of Finance*, 48(1), 65–91.
6. Grinblatt, M., & Han, B. (2005). Prospect theory, mental accounting, and momentum. *Journal of Financial Economics*, 78(2), 311–339.
7. Shapira, Z., & Venezia, I. (2001). Patterns of behavior of professionally managed and independent investors. *Journal of Banking & Finance*, 25(8), 1573–1587.
8. Locke, P. R., & Mann, S. C. (2005). Professional trader discipline and trade disposition. *Journal of Financial Economics*, 76(2), 401–444.
9. LeBaron, B. (2006). Agent-based computational finance. In *Handbook of Computational Economics*, Vol. 2, 1187–1233.

Optional tenth source:

10. Arthur, W. B., Holland, J. H., LeBaron, B., Palmer, R. G., & Tayler, P. (1997). Asset pricing under endogenous expectations in an artificial stock market.

---

## 12. What is still missing from the literature stage

Before final paper prose, two smaller literature questions could still be expanded if needed:

- a direct empirical source specifically on **drawdown-dependent investor behavior** or peak/reference-point effects in portfolio choice;
- a direct source on **professional analyst/advisor sector recommendations** if the paper wants to discuss how such outlooks are produced rather than merely use them as observed external rankings.

Neither is required to begin drafting the Introduction, but they would strengthen the Discussion if time permits.

## 13. Next writing step

After this framework is accepted, draft the **Introduction** and **Behavioral Motivation & Model Design** sections using these sources, while keeping the distinction between literature-supported mechanisms and the project's own stylized parameterization explicit.
