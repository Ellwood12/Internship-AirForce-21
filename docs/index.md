### Introduction

-   The purpose of this guide is to provide adequate examples and
    explanation to why profile likelihood techniques are helpful in
    increasing reliability in confidence based intervals. While going
    through this document, one will be able to input numbers and observe
    comparisons between Profile Likelihood and Wald confidence intervals
    and power.

-   To begin, it will be important to remember that the following
    examples are based on one sample proportion testing. The single
    proportion (or one-sample) binomial test is used to compare a
    proportion of responses or values in a sample of data to a
    (hypothesized) proportion in the population from which a sample data
    are drawn. This is important because we seldom have access to data
    from an entire population.

-   Profile Likelihood testing becomes most vital when the traditional
    requirements for one-sample proportion testing are not met, which
    are: **( *n* being the number of trials, and *p-hat* being the
    observed proportion.)**

$$
\\text{n}\*\\hat{p} \\geq 5 \\\\\\text{and}\\\\\\ \\text{n}\*(1 - \\hat{p}) \\geq 5
$$

-   The profile likelihood method is able to maximize the observed
    sample and thus create bounds that better explain probability when
    the number of successes over total trials get closer to both 0
    and 1. The equation of profile likelihood will be provided later on
    along with other helpful steps.

### Variables

<table style="width:69%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 18%" />
<col style="width: 11%" />
<col style="width: 23%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: center;">NumTrials</th>
<th style="text-align: center;">NumSuccess</th>
<th style="text-align: center;">alpha</th>
<th style="text-align: center;">Hypothesized P</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: center;">11</td>
<td style="text-align: center;">4</td>
<td style="text-align: center;">0.05</td>
<td style="text-align: center;">0.9</td>
</tr>
</tbody>
</table>

### Confidence Intervals

### Graph

![](Binomial_Methods_files/figure-markdown_strict/unnamed-chunk-5-1.png)

### Explanation

The confidence interval is a tool for estimating E{Y}, the “true”
average y-value for a given x-value. This allows us to make better
predictions with decided levels of certain at a given point.  
The way we interpret confidence intervals is unique and may require some
practice. If we were to decide to create confidence intervals of 90%
around a given function, we would say, “We are 90% certain that 90% of
random samples contain the true population parameter”. In this guide,
the focus is on two different types of confidence intervals, the Wald
and Profile Likelihood.

#### Wald Confidence Interval

The Wald interval is the most basic confidence interval for proportions.
Wald interval relies a lot on normal approximation assumption of
binomial distribution and there are no modifications or corrections that
are applied. It is the most direct confidence interval that can be
constructed from this normal approximation.

$$
  {p^\*} \\pm \\space{Z\_{(1-(\\alpha/2)}} \* {\\sqrt{({p^\*} (1 - {p^\*}) / n)}}
$$

#### Profile Likelihood Interval

Profile likelihood is often used when accurate interval estimates are
difficult to obtain using standard methods. In cases where the
likelihood function is not symmetric about the MLE, the Profile
Likelihood Based Confidence Interval serves better. This is because it
is based on the asymptotic chi-square distribution of the log likelihood
ratio test statistic.

Listed below are both the overall equation and the likelihood function.

$$
W = 2\\space \\text{log}(\\text{likelihood}({p^\*}))/\\space\\text{likelihood}(p))\\leq \\chi\_{1-\\alpha}^2
$$

##### Likelihood Equation

function(likelihood) = nSuccesses \* log(*p*) + (nTrials − nSuccesses) \* log(1 − *p*)

### Interval Bounds at (x) Successes

### Graph

![](Binomial_Methods_files/figure-markdown_strict/unnamed-chunk-6-1.png)

### Explanation

The graph produced illustrates how confidence intervals are created for
each x (number of successes) for a Profile Likelihood Confidence
Interval. The upper and lower bounds are discovered where ever the
function crosses 0. What is unique about this processes is the use of
the Chi-square distribution. We are able to make such a statement
because of the testing that appear in the following graphs below.

It is unique how Profile Likelihood creates its bounds as the number of
successes get closer to 0 and 1. Unlike Wald Intervals that dive either
to 0 or 1.0 at the ends, Profile Likelihood allows room for chance to
occur.

### Confidence of The Test

### Graph

![](Binomial_Methods_files/figure-markdown_strict/unnamed-chunk-9-1.png)

### Explanation

This last plot illustrates the performance of the two confidence
interval types. The closer the confidence interval is to the red dashed
line, the more assured we are that our confidence intervals remain
reliable for all probabilities. The Wald Confidence as seen in the plot,
does not remain near the line as the probabilities get closer to 0 and
1. This lets us know that if we want to be (1 - alpha)% confident, we
would do best choosing the Profile Likelihood Test over Wald.

### Power of the Test

### Graph

![](Binomial_Methods_files/figure-markdown_strict/unnamed-chunk-10-1.png)

### Explanation

As printed in the caption below the visual, Power is the probability of
rejecting the null hypothesis H0 when the alternative hypothesis is
true. The power of a hypothesis test is between 0 and 1; if the power is
close to 1, the hypothesis test is very good at detecting a false null
hypothesis.

The graph shown in this section shows the power of each type of
confidence interval for a hypothesized p (p\_H0). What we are looking
for is the type of interval that has the largest power, which turns out
to be Profile Likelihood.

    #https://towardsdatascience.com/five-confidence-intervals-for-proportions-that-you-should-know-about-7ff5484c024f
