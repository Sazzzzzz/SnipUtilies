# Snips

A collection of tools of snippets in VSCode: A handy $\LaTeX$ snippet file, snippet conversion between obsidian and VSCode, and Mathematica snippets for mathematica alias.

<!-- Is the term `Mathematica alias` used correctly? -->
<!-- How to find all mathematica alias without searching -->

## LaTeX Snippet

There are already various snippets available for LaTeX, however snippets are defined in their customized manner, and it might get difficult to get your hands on their snippets by purely reading the code, not to mention the majority of the snippets are regular expressions. So I created my own LaTeX snippets with brief syntax and well documented examples to facilitate easier usage and understanding. They are heavily inspired by OrangeX4 snippets, Mathematica Alias, and some other language syntaxes. 
<!-- Markdown, @ approach from LaTeX workshop -->
For reasons that `soul` package in $\LaTeX$ is fragile and not capitable with Chinese characters or math modes, I use the following command to redefine the `\hl` command:

```latex
\newcommand\hl{\bgroup\markoverwith
{\textcolor{yellow}{\rule[-.5ex]{2pt}{2.5ex}}}\ULon}
```

*(Reference from *LaTeX 入门*)*
