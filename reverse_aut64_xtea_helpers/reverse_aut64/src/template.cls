\LoadClass[a4paper]{report}


\usepackage{amsmath}
\usepackage{mfirstuc}
\usepackage{graphicx}
%\usepackage{geometry}
\usepackage[bindingoffset=10mm,bottom=4cm]{geometry}
%\usepackage{float}
\usepackage{booktabs}
\usepackage[explicit]{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage[nameinlink]{cleveref}
\usepackage{pgfplotstable}
\pgfplotsset{compat=1.18}
\usepackage[per-mode=symbol]{siunitx}
\usepackage[toc,title]{appendix}
\usepackage{url}
\usepackage[section]{placeins}
\usepackage{nomencl}
\usepackage{floatrow}
\floatsetup[figure]{capposition=bottom}
\floatsetup[table]{capposition=top}
\floatplacement{figure}{H}
\floatplacement{table}{H}



\makenomenclature

\AtBeginDocument{\maketitle}
\bibliographystyle{unsrt}

\newcommand\abst[1]{\newcommand\zzabst{#1}}

\newcommand*{\project}[1]{\gdef\@project{#1}}
\newcommand*{\@project}{Graduation Project I}
\newcommand*{\supervisor}[1]{\gdef\@supervisor{#1}}
\newcommand*{\myabstract}[1]{\gdef\@myabstract{#1}}
\newcommand*{\faculty}[1]{\gdef\@faculty{#1}}
\newcommand*{\@faculty}{Engineering}
\newcommand*{\department}[1]{\gdef\@department{#1}}
\newcommand*{\@department}{Mechanical Engineering}

\makeatletter
\AtEndEnvironment{figure}{\gdef\there@is@a@figure{}} 
\AtEndDocument{\ifdefined\there@is@a@figure\label{fig:was:used:in:doc}\fi} 
\newcommand{\conditionalLoF}{\@ifundefined{r@fig:was:used:in:doc}{}{\newpage\listoffigures}}%
\makeatother

\makeatletter
\AtEndEnvironment{table}{\gdef\there@is@a@table{}} 
\AtEndDocument{\ifdefined\there@is@a@table\label{tab:was:used:in:doc}\fi} 
\newcommand{\conditionalLoT}{\@ifundefined{r@tab:was:used:in:doc}{}{\newpage\listoftables}}%
\makeatother

\makeatletter
\renewcommand*{\maketitle}{%
  \begin{titlepage}
  \newgeometry{bindingoffset=10mm,bottom=3cm}
  {\centering\includegraphics[scale=1.2]{logo}\par}
  \vspace{1cm}
  \centering
  {\scshape\LARGE Université de Paris 8 \par}
  \vspace{1cm}
  {\Large\xcapitalisewords Faculté d' {\@faculty}\unskip\strut\par}
  \vspace{1cm}
  {\Large\xcapitalisewords Département de {\@department}\unskip\strut\par}
  \vspace{2cm}
  {\scshape\Large\@project\unskip\strut\par}
  \vspace{1.5cm}
  {\huge\bfseries\xcapitalisewords{\@title}\unskip\strut\par}
  \vspace{2cm}
  {\Large\xcapitalisewords{\@author}\unskip\strut\par}  
  %\vfill
  %Supervised by\par
  %\@supervisor\unskip\strut\par
  \vfill
  {\large \@date\par}
  \end{titlepage}
  \newpage
\pagenumbering{roman}

\begin{abstract}
\zzabst
\end{abstract}

\tableofcontents
%\listoffigures
%\listoftables
\conditionalLoF
\conditionalLoT
\printnomenclature
\newpage
\pagenumbering{arabic}
}
\makeatother

\usepackage{etoolbox}
\patchcmd{\abstract}{\null\vfil}{}{}{}

\renewcommand{\bibname}{\raggedright Références}

\titleformat{\chapter}[display]{\bfseries\centering}{\huge \chaptertitlename\ \thechapter}{1em}{\Huge #1}
\renewcommand{\contentsname}{\raggedright Sommaire}
\renewcommand{\listfigurename}{\raggedright Liste des Figures}
\renewcommand{\listtablename}{\raggedright List of Tables}


\pgfplotstableset{
    every head row/.style={
    before row=\toprule,after row=\midrule},
    every last row/.style={
    after row=\bottomrule},
    col sep = &,
    row sep=\\,
    string type,
}

\newcommand{\entries}{\pgfplotstabletypeset}

\newtoggle{appendixbib}
\pretocmd\appendix{\toggletrue{appendixbib}\bibliography{ref}}{}{}
\AtEndDocument{\iftoggle{appendixbib}{}{\bibliography{ref}}}

%\let\origfigure\figure
%\let\endorigfigure\endfigure

%\renewenvironment{figure}[1][H]{%
%	\origfigure[#1]%
%	\centering
%}{%
%	\endorigfigure
%}

%\let\origtable\table
%\let\endorigtable\endtable

%\renewenvironment{table}[1][H]{%
%	\origtable[#1]%
%	\centering
%}{%
%	\endorigtable
%}

