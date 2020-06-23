{% include mathjax.html %}


When \\(a \ne 0\\), there are two solutions to \\(ax^2 + bx + c = 0\\).

$$\left(\sum_{i=1}^{n}{\left|a_i\right|}^p\right)^{1/p}$$

u&=x^2+3, $ so that $ \, \frac{du}{dx}=2x &\\
\int & 4x\cdot e^{u}\, \frac{du}{2x} =  2\int e^u \, du = 2e^{x^2+3}+C &\\
\intertext{We now evaluate the limits}
\int\limits_0^1 & 4x\cdot e^{x^2+3} \, dx = 2\left[ e^{x^2+3} \right]\limits_0^1 = 2e^4-2e^3 &
\end{flalign*}
\item $\displaystyle \int \frac{x-6}{x^2-4}  \, dx \\$
\begin{flalign*}
\intertext{We use the method of partial fractions}
&\frac{x-6}{x^2-4} = \frac{A}{x+2}+\frac{B}{x-2}&\\
&(x-6)  = A\cdot(x-2) + B\cdot(x+2) &\\
&\intertext{Which gives $A=2$ and $B=-1$, so that}
&\int \frac{x-6}{x^2-4}\, dx = \int \frac{2}{x+2} + \frac{-1}{x-2}\, dx = 2ln|x+2|-ln|x-2|+C &

{% include disqus.html %}
