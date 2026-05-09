# paper/figures/

Figures used by the paper. Two conventions:

- **One `.tex` fragment per figure.** The fragment contains the
  `\includegraphics` line on the first line, followed by the
  `\caption{...}` and `\label{fig:...}`. Sections include figures with:

  ```latex
  \begin{figure}[H]
      \centering
      \input{figures/<name>}
  \end{figure}
  ```

  This keeps figure code self-contained: if you reuse a plot in a talk,
  you take the one `.tex` file with you.

- **Binary asset alongside the fragment.** PDF for vector figures
  (preferred), PNG for screenshots and bitmaps. Name the binary the
  same as the `.tex` fragment (e.g. `dispersion.pdf` paired with
  `dispersion.tex`). Drawio sources may live next to the exported PDF
  if you generate figures from `.drawio` files.

Generation scripts that produce figure binaries should live in
`src/utilities/` (in the full-stack template) and emit their output
here. Add a comment at the top of each fragment naming the script that
generated the binary, so future-you can rebuild the figure.
