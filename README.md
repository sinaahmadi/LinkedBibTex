# LinkedBibTex
## A solution to make your BibTex files automatically

This is repository provides a simple solution **to automatically create and manage your bibliography file** in [`BibTex`](https://en.wikipedia.org/wiki/BibTeX) using [DBLP](https://dblp.org). It saves author's time of modifying your `.bib` file back and forth. Here it is how it works:

Each entry on [DBLP](https://dblp.org) has a unique identifier called `dblp key` which is provided down below the export button of each article (see [this article](https://dblp.org/rec/journals/cacm/Knuth74), for example). When citing a reference, the author cites using `dblp key` as in `\cite{dblp key}` without importing the bibliographic entry in the `.bibtex` file. This solution creates the `.bib` file automatically for you when compiling the `.tex` file and the author would not need to import bibliographic data manually any more.

#### Requirements
- Python
- [DBLP's API](https://dblp.org/faqHow+to+use+the+dblp+search+API.html)
- [bibtex-dblp](https://github.com/volkm/bibtex-dblp)

## How to use this?

Nothing is going to change with the way you prepare your document in `Tex` or the way you cite your references. However, there is one additional step that should be taken into account when compiling your files.

Normally, compiling a `Tex` file with bibliography looks like the following in the command-line:

    pdflatex -> bibtex -> pdflatex -> pdflatex

To create the file of references automatically, the following command is to be added:

	makebib -> pdflatex -> bibtex -> pdflatex -> pdflatex
    
Here is an example where we want to compile the following document (which is called `article.tex`):

	\documentclass{article}
	\begin{document}
		This is an example to cite a few papers such as
		\cite{journals/algorithms/Lucena-SanchezS21} and
		\cite{journals/sqj/GiraldoCEP21,conf/eacl/SinghVGS21}.
	
	\bibliographystyle{unsrt}
	\bibliography{references}
	\end{document}

Now, compiling of your file would look like this:

	python makebib.py article.tex
	pdflatex article.tex
	bibtex article
	pdflatex article.tex
	pdflatex article.tex


## What's next?

I believe that this project is yet to become truly functional. Here are a few ideas:

- Creating **a centralized bibliographic database** to facilitate data retrieval, particularly via an API or SPARQL endpoint. Unfortunately, [Google Scholar](https://scholar.google.com/) as one of the major bibliographic databases does not seem to provide such required functionalities for more inter-operable services. Although [DBLP](https://dblp.org) does an amazing job with its API, it does not include material from other fields but Computer Science.
- Support from other cloud-based LaTeX editors such as [Overleaf](https://www.overleaf.com). Many users may not even be able to install Python on their computer.
- I tried to find a way to use the current solution as a package in `Tex` to be imported directly with the `.tex` file. I couldn't find an appropriate solution (tried [PythonTeX](https://github.com/gpoore/pythontex), too). If you have any idea, let me know 🙂


