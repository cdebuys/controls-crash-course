// MathJax config for pymdownx.arithmatex (generic mode), which wraps math in
// \( \) / \[ \] inside elements with the "arithmatex" class.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};
