[DOI: 10.1111/cgf.14309](https://doi.org/10.1111/cgf.14309)


Eurographics Conference on Visualization (EuroVis) 2021
R. Borgo, G. E. Marai, and T. von Landesberger
(Guest Editors)



_Volume 40_ ( _2021_ ), _Number 3_


# **A Deeper Understanding of Visualization–Text Interplay in** **Geographic Data-driven Stories**

Shahid Latif _[†]_ [1], Siming Chen _[‡]_ [2], and Fabian Beck _[§]_ [1]


1 paluno, University of Duisburg-Essen, Germany
2 School of Data Science, Fudan University, Shanghai, China


**Abstract**

_Data-driven stories comprise of visualizations and a textual narrative. The two representations coexist and complement each_
_other. Although existing research has explored the design strategies and structure of such stories, it remains an open research_
_question how the two representations play together on a detailed level and how they are linked with each other. In this paper,_
_we aim at understanding the fine-grained interplay of text and visualizations in geographic data-driven stories. We focus on_
_geographic content as it often includes complex spatiotemporal data presented as versatile visualizations and rich textual_
_descriptions. We conduct a qualitative empirical study on 22 stories collected from a variety of news media outlets; 10 of_
_the stories report the COVID-19 pandemic, the others cover diverse topics. We investigate the role of every sentence and_
_visualization within the narrative to reveal how they reference each other and interact. Moreover, we explore the positioning_
_and sequence of various parts of the narrative to find patterns that further consolidate the stories. Drawing from the findings,_
_we discuss study implications with respect to best practices and possibilities to automate the report generation._



**1. Introduction**


Data-driven stories presented in online articles combine the expressive power of visualizations with a textual narrative. In these stories, visualizations provide an overview of the data while the accompanying text highlights insights and blends in the backdrop of
the story. Both representations—visualization and text—are closely
related and complement each other. It is found that the spatial arrangement and interactive linking of both representations influence
the readers’ engagement, comprehension, and recall of information [OKCP19, ZOM19]. Existing research has already explored
the design space of distinct design strategies, overall structuring,
and interactivity within such stories [SH10]. However, the focus
stays rather broad and we lack an in-depth classification of the textual content according to its role in the story and how different parts
of the text connects with the visualization. Better understanding of
this fine-grained interplay between visualization and textual narration can reveal best practices of such stories and inform research
supporting their creation.


Stories relating to geographic data are particularly interesting to
study as the spatiotemporal nature of data makes the reporting challenging. Unlike reporting plain time series (e.g., the revenue of a


_†_ shahid.latif@paluno.uni-due.de

_‡_ simingchen@fudan.edu.cn
_§_ fabian.beck@paluno.uni-due.de


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John
Wiley & Sons Ltd. Published by John Wiley & Sons Ltd.



company) or results of public-opinion polls, it usually requires multiple visualizations to show different aspects of the spatiotemporal
data; some with a geographic focus and others with a temporal one.
We find examples of geographic narratives across diverse journalistic branches such as politics, economics, science, and health. The
current COVID-19 pandemic further provided the unique opportunity to collect various polished examples from the same context.


The main objective of this research is to achieve a more accessible and self-explanatory data reporting and to support journalists and visualization experts with a set of best practices to make
their stories adaptable to the interests of the individual readers. To
do so, we aim at understanding the fine-grained interplay of geographic visualizations and textual narration through an empirical
analysis of a selection of data-driven stories. We investigate the role
of every sentence within each of the narrative categories and how
sentences are interwoven with the visual representation. Besides,
we explore the positioning and sequential patterns among various
parts of the stories. In particular, we seek to answer the following
research questions:


_•_ **Q1** : What are the reported analysis insights and how is the related data visually communicated?


–
**Q1.1** : What are the analysis insights presented in the textual
narrative and how is context blended with these insights?

–
**Q1.2** : How are geographic and non-geographic visualizations
used as a complement to communicate the data?


_•_ **Q2** : How do textual narration and visualization interplay?


312



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



– **Q2.1** : What links exist between the two media?

–
**Q2.2** : How and in what sequence are visualizations embedded into the narrative?


We perform a qualitative analysis of 22 stories collected from a
variety of well-known news media outlets. We analyzed 1,203 sentences and 118 visualizations contained in these stories and struc
tured them according to a detailed coding scheme. Based on the
assigned codes, we are able to answer the above research questions. To provide actionable insights, we discuss the implication of
the results along best practices for authoring such stories as well
as options for their personalization and automatic generation. To
ease re-usability and extension, we make all study data available
as supplemental material, along with our interactive visualization
(presented in Figure 3) for exploration.


**2. Related Work**


We review existing literature in regard to similar empirical studies
for understanding various aspects of narrative visualization, support and authoring tools for story generation, and techniques to link
the textual and visual representations.


**2.1. Narrative Visualization**


Narrative visualization—also known as data-driven storytelling—
combines a textual narrative with visualizations to communicate
analysis results [RHDC18]. Tong et al.’s [TRB _[∗]_ 18] extended survey provides a comprehensive overview of storytelling techniques
in visualization. Studying existing stories can inform effective presentation strategies and the design of authoring tools for narrative visualizations. Researchers have already explored stories regarding various storytelling scenarios [KM13], the design space
of distinct genres and role of interactivity in data stories [SH10,
BWF _[∗]_ 18], structure and sequencing [HDH _[∗]_ 13], and even immersion [ILQC18]. Several researchers have performed empirical qualitative research. Among these, Segel and Heer [SH10] analyzed
design strategies and interactivity in narrative visualizations that
were published in news media. Hullman et al. [HDH _[∗]_ 13] investigated 42 professional narrative visualization examples to understand the sequences in these stories and inform the design of
an authoring tool for identifying effective sequencing of visualizations. Hullman et al. [HKL17] explored different structuring
strategies people followed to arrange a set of given related visualizations into a sequence as part of a user study. Similarly,
McKenna et al. [MHRL _[∗]_ 17] systematically examined the characteristic factors—relating to story layout, navigation, role of visualizations, and level of control—of narrative visualization that play
an important role in how users read and interact with the stories.


Existing research also addresses the authoring of data-driven
stories. The corresponding approaches can be broadly classified
into two types. First are the ones that support manual creation
of data stories. Among these, _DataClips_ [AHRL _[∗]_ 17] provides an
authoring interface for data videos with different templates that
users can customize. _Data Illustrator_ [LTW _[∗]_ 18] supports data
binding to expressive charts for making data stories memorable.
Ren et al. [RBL _[∗]_ 17] discuss the design space of annotations and
present an interactive tool to create such annotations. Brehmer et



al. [BLHR _[∗]_ 19] facilitate the authoring of timeline narratives. In
contrast, the second type of authoring approaches provide automatic support. Among these, _Datashot_ [WSZ _[∗]_ 19] automatically
derives data facts from tabular data and generate infographics to
provide an overview. _Calliope_ [SXS _[∗]_ 21] supports automatic generation of a story sequence directly from a given dataset. Metoyer
et al.’s [MZJS18] approach automatically integrates short textual
annotations at various points on the visualization when users highlight a passage of text.


Although text is a vital part of narrative visualizations, we still
lack an in-depth understanding of what different roles it plays and
how it interacts with the visualizations; existing research focuses
less on characterizing the textual narrative in a story.


**2.2. Linking of Visualization and Text**


Researchers have explored different ways to better connect the text
and visualization. Goffin et al. [GBWI17] investigated the design
and usage of word-scale graphics and micro visualizations that
can be embedded in text documents. Latif and Beck [LB18] presented further possibilities to extend word-scale graphics to represent spatiotemporal data. Beck and Weiskopf [BW17] proposed
the idea of a two-way interactive linking between text and (wordscale and regular) visualizations—hovering a text fragment highlights the relevant part of a visualization and vice versa—, also suggesting that this might support multiple reading strategies. Mumtaz
et al. [MLBW20] developed a visual analytics solution for describing the code quality of a software, where generated text is regarded
as a representation in a multi-view system that can be brushed and
linked like any other visualization. In their system, visualization
captions adapt while interacting with the visualizations. Other systems link generated textual explanations with visualizations in different context, for instance, to report analysis findings (e.g., _Vis Au-_
_thor Profiles_ [LB19b]) or to explain causality visualizations (e.g.,
_CauseWorks_ [CSC _[∗]_ 21]).


Existing research has also studied the impact of document layout
and interactive linking on readability and comprehension. Ottley et
al. [OKCP19] found that people often have a hard time consolidating the information that is presented across the two media and suggested the need of a more effective representation. In a controlled
experiment, Zhi et al. [ZOM19] discovered that participants recall
information better when it is interactively linked across the two media. Barrel et al. [BLC20] studied the impact of adaptive guidance
on the readability. The guidance is provided, for instance, by visually highlighted bars of a bar chart based on participants’ eye fixation to a sentence in the narrative. It was found that this adaptive
guidance helps improve comprehension particularly among participants with low visualization literacy.


As the linking of text and visualization influence how readers
consume information, we believe that a deeper investigation of the
visualization–text interplay can inform design strategies for achieving an even better integration of the two media.


**3. Methodology**


To answer the research questions (Q1 and Q2 in Section 1),
we adopt a similar approach as applied in several existing


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



313



**Figure 1:** _Sources of stories in our data collection._


works [SH10, HDH _[∗]_ 13, MHRL _[∗]_ 17]. We performed a qualitative
analysis on 22 geographic data-driven stories. We decided to follow a qualitative approach focusing on fewer examples but a finegrained and deep analysis because we were more interested in finding possibilities and best practices. This is also why the stories
should have high quality, both with respect to its textual narration
and visual data representation. Going down to sentence-level analysis of the text and fine-grained characteristics of the visualizations
allows us to reason about the details of spatiotemporal data representation as well as linking and referencing between text and visualizations.


**3.1. Data Collection**


The 22 stories were collected from 10 well-known digital journalistic sources including New York Times (NYT), FiveThirtyEight
(538), and BBC; the full list of sources is shown in Figure 1. The
stories are published between 2016 and 2020. Our story selection
criteria involved the presence of at least one geographic visualization and a comparable proportion (in terms of screen real estate)
of textual and visual narrative. Another but less strictly applied criterion was the presence of interactivity. We began with searching
for stories that contained visualization–text interactions (e.g., interacting with text visually highlights the relevant part of the visualization or vice versa). Having found only 3 such stories, we
loosened the criterion of interactivity to visualizations alone in the
story. Later, we also included 7 stories that did not offer interactivity. In our sample collection, fifteen out of 22 stories offer some
form of interactivity.


In the first phase, we picked 12 stories (Collection A) on a variety
of themes such as culture, economics, politics, science, and health
to maximize the diversity of topics. In the second phase, we chose
another 10 stories (Collection B) on a single topic: the COVID19 pandemic. These 10 stories have the same context yet covering
various aspects of the pandemic. The two collections complement
each other; one embraces diversity while the other focuses on certain comparability.


**3.2. Qualitative Analysis**


Every story was divided into individual sentences and visualizations. This resulted in 1,203 sentences and 118 visualizations for
22 stories (638/66 for Collection A and 565/52 for Collection B).


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.



We followed an open coding approach. The coding (i.e., labeling
the sentences and visualizations) proceeded as follows: two coders
(both coauthors of this paper) used 4 stories from Collection A as
seeds and independently assigned descriptive codes to sentences
as well as visualizations. In a follow-up meeting, the codes were
discussed; similar codes were merged and conflicting code assignments were resolved. This initial coding scheme was then rolled out
to the rest of the eight data stories in Collection A. For this, we followed a sequential process: one coder did the coding first, and then
the other coder checked and refined the first coding. The analysis of
Collection A provided us with a code taxonomy that was then verified and further fine-tuned with its application on Collection B. We
followed the same process to analyze stories in Collection B. Over
the course of several meetings, we kept on resolving and consolidating the codes and categories, ultimately resulting in 45 distinct
codes across 4 categories and 12 subcategories.


Overall, this resulted in 25 codes for sentences and 20 codes for
visualizations (cf. Figure 2). In total, there are 1,812 code assignments for sentences and 569 for visualizations. Our coding scheme
allowed for multiple code assignments to a sentence or visualization. We group these codes along the categories _**data-driven**_ text
and _**embedding**_ for textual narrative (sentences), _**visualization**_ for
visualization-specific codes, and _**visualization–text linking**_ for the
interplay between the two media (e.g., a sentence that references
a visualization or a visualization that has a textual annotation). As
shown in Figure 2 (leftmost column), the colored coding categories
have further subcategories that will be discussed along reporting
of the results. All codes and code categories are always underlined
with the respective color in the following for an improved readability and figure–text linking, while categories and subcategories are
printed in bold font to discern them from codes.


**4. Results: Insights and Visual Communication (Q1)**


First, we study the ingredients of the stories, namely the individual
sentences and visualizations. Figure 2 gives a qualitative overview
of what these ingredients are, but also reports related quantities
(i.e., how frequently a certain code is assigned). These quantities
are not meant to generalize beyond a specific story but help us
judge the general character of a story (e.g., working a lot with direct
quotes) and find interesting outliers (e.g., a unique style of reporting). In the following, we systematically discuss these ingredients
along the code categories and subcategories, clarifying their meaning as well as describing their typical use and remarkable examples.


**4.1. Analysis Insights and Context (Q1.1)**


Generally, we observe two main categories of **textual narrative** in
the data-driven stories: the actual _**data-driven**_ text and the text that

serves as the _**embedding**_ in the story, for instance, structuring text
like headings or contextual information like dataset descriptions.
_**Data-driven**_ text does not just list the raw numbers but summarizes
analysis findings at a higher level as _insights_ . Although there seems
to be no agreed definition of an _insight_ in visualization community [CZGR09], it may be defined as _“complex, deep, qualitative,_
_unexpected, and relevant”_ [Nor06] or _“an individual observation_
_about the data [...], a unit of discovery”_ [SND05]. In the following, we define an _insight_ as non-trivial, qualitative, and relevant


314



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



A01 A02 A03 A04 A05 A06 A07 A08 A09 A10 A11 A12 B01 B02 B03 B04 B05 B06 B07 B08 B09 B10


Source 538 538 538 538 REU 538 FT NYT WP WP MSN NYT BBC CNN NYT NYT NYT ONS GUA NYT BBC BBC





**Figure 2:** _Frequencies of codes for 22 stories on sentence- and visualization-level, structured by code categories and subcategories. Gray-_
_blue background encodes the frequency of sentences, yellow background the frequency of visualizations. Multiple codes can be assigned to_
_a single sentence/visualization, hence, per story, the total count of sentences and visualizations does not correspond to the total number of_
_assigned codes._
_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



315



observation about the data. An example of an insight from A02 is:
_“[i]n some states, like Montana and Alaska, nearly the entire adult_
_population is registered [as organ donors].”_


In geographic stories, _**geotemporal**_ entities— _location_ and
_time_ —are usually key terms of the textual description of the insights. Almost all stories contain (20 of 22; see Figure 2) identifiers
of _locations_ . While most locations are referenced by their specific
names (e.g., _“Boston”_ – A09, _“Massachusetts”_ – A02, _“USA”_ –
B09), a variety of collective terms according to geopolitical, geographic, or administrative units are also used. For instance, A01 describes counties suffering high casualties as: _“[r]ural Appalachia_
_stands out; nine counties in Kentucky and three in West Virginia_
_make the list.”_ Appalachia is a region in the eastern US and is
not marked on the map visualization; reader’s knowledge is presumed. Other variations include _“Dakotas”_, _“among the peaks of_
_Rocky Mountains”_ (A01), and _“Midwest”_ (A02). The directional
phrases such as _“west of the Mississippi”_ (A01) and _“southern_
_tip of Bangladesh”_ (A05) are another way of referencing location.
_Time_ identifiers are also frequent in our examples, but not as frequent as location identifiers (contained in 16 vs 20 stories; 61 vs.
144 occurrences). Depending on the data, time may be identified
at various levels of granularity (e.g., day, month, year, decade, or
even century). Time identifiers include fix dates (e.g., _“on April_
_30”_ – A02), longer events (e.g., _“Hurricane Katrina along the Gulf_
_Coast in 2005”_ – A04), or time intervals (e.g., _“since 1980”_ – A01,
_“from 2000–2016”_ – A04, _“past decade”_ – A09, _“1970s”_ – B01).
Consecutive sequences of timely events may span across multiple
sentences. For instance, _“By Nov 8, [...] By mid-October, [...] As of_
_Nov 26, [...]”_ – A05).


A specific type of insights _**identifies**_ interesting data items as _out-_
_liers_, _extrema_, and _clusters_ . We observe locations that are local or
global _outliers_ . The former compares a location with its neighbors
while the latter characterizes it with a much larger geographical region. For instance, A04 states a local outlier as: _“Only two rural_
_counties in the entire area that stretches from Mississippi across_
_to Florida [...] even crack the list [...].”_ A temporal outlier highlights unique temporal behavior: _“[f]or the first time in more than_
_50 years, the majority of America’s public school children are liv-_
_ing in poverty”_ (A11). An example of a geotemporal and global
outlier in A10 is _“California has had more of these public mass_
_shootings than any other state.” Extrema_ correspond to the locations assuming the maximum or minimum values of a data variable. They are closely related to outliers. In most cases, outliers are
extrema having specific importance with respect to a geotemporal
variable. A _cluster_ refers to a group of locations showing similar
values for one or multiple data variables. Clusters include a list of
two or more locations ( _“North and South Dakota”_ – A01) or refer
to higher level of grouping (e.g., _“Dakotas”_ – A01, _“Midwest”_ –
A02). Clusters are described with the metric on the basis of which
they are identified. For instance, _“counties with the lowest mortal-_
_ity rates, 18 out of 20 fall west of the Mississippi”_ (A01) refer to a
cluster of counties showing specific values of mortality rates.


_**Summarize**_ insights report _geographical variation_, _average_ (i.e.,
mean, median, or mode), or _temporal variation_ . A _geographic vari-_
_ation_ reports the varying value of a variable across a geographic
region. For instance, _“[t]he South and West of the country [...] seen_


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.



_a big rise in the number of infections”_ (B10). It mostly summarizes those variations that are peculiar. To describe the _average_, less
technical words such as _“average values”_, or _“on average”_ (e.g.,
_“[e]ach year, about 8,000 people will get that chance”_ – A02) are
widely used. Statistical terms like _“median”_ or _“mean”_ were also
observed. It was surprising to see that some stories describe even
the statistical significance: _“What is more, unemployment, while_
_being statistically significant across the country, was not associ-_
_ated with the Le Pen vote in urban areas”_ (A07). _Temporal vari-_
_ations_ correspond to the reporting of a time series. We observed
more instances of the reporting of peaks, nadirs, and steep inclination or declination, for instance, _“[...] demand for energy globally_
_has fallen off a cliff”_ (B01). Long term trends are also noted like
_“[...] trend in demand has been downhill ever since”_ (B01). Portions of a time series are compared with other portions specifically
the ones that are recurrent and show seasonal patterns: _“[t]his com-_
_pares with 73% last week and a peak of 85% between 3 April and_
_13 April 2020”_ (B06).


_**Compare**_ insights deal with _part-to-whole_ comparisons, report
_correlation_, and _rank_ . _Part-to-whole_ insights refer to a proportion
of a total (e.g., 20% of the counties). These proportions are reported
as exact percentages (e.g., _“23.5 percent”_ – A11) or rounded (e.g.,
_“more than half”_ – B08, _“one-third”_ – B06). While reporting a
countable variable—for instance, number of participants of a survey in B06—we observed the use of a reference of ten (e.g., _“4 in_
_10”_ to describe 41 percent of participants). The use of quantifiers
like _“vast majority of the counties”_ (A01) is another way of describing proportions without giving exact numbers. More than half
of the part-to-whole comparisons are in B06—it communicates the
results of a survey to gauge the social impact of COVID-19 in Great
Britain. The _correlation_ insights refer to the reporting of relationships between multiple variables. They include descriptions of positive or negative relationships and discuss causality. For instance,
A07 discusses the impact of various socio-economic parameters
(e.g., education, income) that played a role in French elections. It
goes beyond comparing two variables and discusses intersection effects: _“[w]hile areas with higher median annual income were more_
_likely to vote disproportionately for the centrist candidate, the ef-_
_fect of income is negated when education is taken into account.”_ .
Moreover, _rank_ insights report the order of data entities with respect to a variable, for instance, _“Brazil reported more than 32,000_
_new cases on Wednesday, the most in the world, and the United_
_States was second [...]”_ (B03). These insights may not always reflect the numeric ranks but may also use comparative words, for
instance, _“[...] black workers seem to be struggling far more than_
_white or Hispanic workers”_ (A04).


A considerably large portion of the textual narrative integrates
different types of _**embedding**_ (see Figure 2). A part of this embedding are the sentences that _**structure**_ the story. All stories begin
with a title (a type of _heading_ ; here, colored differently as black
is later used to better discern sections in Figure 3). In 11 stories,
the title serves as the main driving question of the story (e.g., A02,
A04, B04). Five of the stories have a title that conveys the main
takeaway (A02, A03, A07, A08, B08). Thirteen stories also contain additional _driving_ _questions_ (25 in total and 20/25 for stories
of Collection A) at various positions in the narrative. _Transitional_
sentences or _headings_ are a way to switch between different topics.


316



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



_**Context**_ is another form of embedding and provides additional
information and opinion. All stories include _background_ that may
help readers better understand the story and data. For instance, before reporting how organ donation system works, A02 first describe
the causes and symptoms of liver cancer. In rather technical stories
like A02 or A03, the specific technical terminology and other related concepts are explained as _domain knowledge_ . For instance,
A03 uses a third of the narrative to explain the concepts of production and audibility of seismic waves. Stories in Collection B
describe the impact of COVID-19 where only a few sentences introduce domain knowledge. _Dataset descriptions_ include information on who gathered the data, how it was collected, and whether
it was preprocessed or filtered for a specific reason (e.g., _“[a]reas_
_with very low populations were removed to limit their potential to_
_skew the analysis”_ – A07). Almost 80% (18/22) of the stories include direct (40) and indirect (100) _quotes_ . We observed two main
sources of these quotes. One source is researchers who worked on
the problem and gathered the data (e.g., in A03, A08, A12, B05).
In such quotes, they share the methodology, insights, eureka moments of their research, or describe the findings. The second source
of the quotes is the policy makers (e.g., in A02, B10). These quotes
included their opinions or implications. Eleven of the stories include _external references_, for instance, to the full dataset, a research
paper, or another story. _Interpretations_ connect insights with historical facts: _“American Indian populations have historically suf-_
_fered from poor health outcomes and challenges in health care ac-_
_cess, contributing to high mortality rates.”_ (A01). Or they infer
and deduce other insights: _“[i]f you’re a New Yorker, that doesn’t_
_seem very fair”_ (A02). Authors also attach their personal _judgment_ :
_“[o]rgan donation is good and kind, but it isn’t fair”_ (A02).


**4.2. Visual Communication (Q1.2)**


While the textual narrative explicitly explains the analysis insights,
visualizations complement the text by showing relevant data. In our
collection, 45 visualizations offer interactive exploration capabilities in 13 out of 22 stories. We found, that unless annotations are
made, it stays up to the reader to find insights. Still, the authors
of a story select a certain way to visually communicate the data.
The **visualization** category in Figure 2 shows the codes regarding _**type**_, _**purpose**_, and _**exploration**_ of the visualizations, as well as
whether they carry a _legend_ or _visual annotation_ ( _**properties**_ ). In
our collection of 118 visualizations, we identified 8 distinct types
of visualizations and 4 main modes of exploration.


First, we try to identify for what main _**purpose**_ a visualization
was included in the story. Although we do not know the original
intentions of the authors, we were able to roughly categorize the
visualizations into _overview_, _detail_ (with respect to certain aspects),
and _comparison_ visualizations. One visualization can share two or
more purposes, for instance, provide overview as well as facilitate
comparison. We do not discuss the purposes separately, but mixed
with the following discussion of visualization _**types**_, as both coding
subcategories interact.


We observe that every story includes an _overview_ visualization as
the first visual data representation. A _map_ visualization is a straightforward way of providing an overview of geographical data which
more than half of the stories (13/22) contain as the first visualiza


tion. We classify these _maps_ as statistical (31) and geographical
maps (5). Statistical maps are either thematic maps encoding data
as colored regions (18)—also known as choropleths—or encode
data in glyphs (e.g., circles, rectangles, or other markers) overlaid
on the map (13). Geographical maps, on the other hand do not encode any additional data. Satellite images or a street view are examples of such maps. Maps, particularly choropleths are mostly
restrictive to a single variable and may not allow for comparisons
across multiple variables. However, multiple versions of choropleth
maps (5 in Collection A, 2 in Collection B) placed next to each
other (or side by side) allow for _comparisons_ of multiple variables.


_Tabular_ visualizations (13) provide both _comparison_ and
_overview_ . All tables in our collection either use visual encoding—
as font color or cell backgrounds—or embed micro visualizations.
Often, they communicate variation or uncertainty (e.g., distribution) in addition to, for instance, sum or average values. See two
such tables from A01 below:


Besides the overview and comparison of aggregated geographical data, another aspect is the communication of geotemporal variations. Animating the map visualization is one way of accomplishing it; we observed five such instances. In tables, micro line plots
show the temporal variations of geographic entities that have been
arranged in rows of the table (see the right table above). Beyond
maps and tables, small multiples are another way of providing
geotemporal overview and comparison. We mostly observed the
use of _line_ and _area_ charts in small multiples. For instance, three
such examples are shown below (taken from B01, B03, and B07
respectively):


Including a time series next to a map visualization is yet another
way to simultaneously communicate both geographical and temporal aspects. In such cases, the map displays the aggregated values
for a certain time span while the line plot shows temporal variations across that time span. Multiline plots (e.g., B02-V4 in Figure 3) can also provide comparisons across geotemporal data. Each
geographic region (e.g., a city, state, or country) is denoted by a
separate line and a specific region can be highlight—on hover—to
allow comparisons with all other regions (B02). We also observe
the use of a rather non-standard (overlapped) _area_ plot for showing
a temporal overview (A10); the below timeline visualization shows
the lives lost during various mass shootings in the US. Purple semi
circles denote the number of people killed compared to the ones
injured shown as light gray semi circles.


_Bar_ plots offer comparisons across different categorical variables and include simple bar plots (6), group bar charts (2), and
stacked bar charts (8). Stacked bar charts can provide part-to-whole
comparisons as well. For instance, B06 uses many bar charts to report the results of a survey on the social impact of the COVID-19
pandemic in Great Britain.


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



317



The _detail_ visualizations go deeper with respect to certain aspects of the data analysis. In our collection, we observe the use
of _point_ plots (e.g., scatter plots), _distribution_ plots, and _diagrams_ .
Distribution plots are limited to univariate data and include histograms (15), dot plots (2), and range plots (3). Comparatively,
many more detail visualizations are observed in A05, A07, and
B06. For instance, A07 reports the French presidential election
results; the story begins with a spatial overview and comparison
of votes for both candidates (one choropleth for each candidates
placed side by side). The story, then, discusses various predictors
that played a role in the election. A Sanky _diagram_ illustrates the
shift of allegiances of voters between the first and second round
of the election. Similarly, Beeswarm distribution—a type of dot—
plot compares the distribution of voters for the candidates across
multiple social parameters (e.g., education, income, etc.).


Furthermore, scatter plots with trend lines show the correlation
of votes with respect to education level and income of voters.


We observed the use of infographics in some visualizations especially in A10 and B01. A10 uses gun icons to give an impression
of the kind of weapons used in mass shootings. Similarly, avatars
of 1,204 victims and 183 shooters visually communicate their age
(e.g., child or adult) and gender; users can hover to get details about
each victim or shooter. Similarly, flags of two countries (US and
France) serve as intuitive labels in a comparison area plot in B01.


About a third of the visualizations (44/118) allow for interactive
_**exploration**_ . The simplest form of exploration is to offer details-ondemand as a _tooltip_ (16/44). Eight visualizations (all maps) offer
_multiple scale zooming_ allowing readers to explore the data at various levels of geographical granularity; for instance, first provide an
overview on the state level and then the city or county level. Almost
half of the interactive visualizations (20/45) offer a _data selection_

_control_ . It lets readers choose a data dimension of their interest. The

visualizations in A06, A10, and B05 are attached to a single central
data selection control. While B05 just highlights the selected data
object (e.g., a city) in all linked tabular visualizations, A06 and A10
include multiple views showing different aspects of the data. Five
visualizations (all maps) include a _time slider_ to play or pause an
animation.


**5. Results: Interplay of Text and Visualization (Q2)**


Based on the ingredients discussed above, we can now study the interplay between visualizations and text, more specifically, the various ways of linking the textual and visual representation as well as
their joint organization in one story.


**5.1. Linking the Two Media (Q2.1)**


Links between visualization and text can be explicit or implicit.
This section focuses on reporting the explicit links that can be unambiguously identified. We also noticed various ways of implicit


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.



links during our analysis, but they are vaguer and more ambiguous, hence, we could not include them into our coding scheme.
For instance, just co-referencing the same identifier or any data insights from the visualization and the text creates such implicit links.
Moreover, positioning the visualization close to the related text, the
two are likely perceived as belonging together (the positional interplay of the two media is discussed in more detail for Q2.2). With
respect to the explicit links, we discern two subcategories of codes
as described in the following and summarized in Figure 2.


First, _**text-in-vis**_ linking blends in textual content inside a visualization and includes _captions_ (also comprising visualization titles),
_annotations_, and _tooltips_ . Almost 86% of the visualizations in our
collection include a descriptive caption. The length of a caption
may vary with the complexity of a visualization. We also observed
that captions are more expressive in complex and non-standard visualizations, for example, Sankey diagram, and beeswarm plot in
A07. In 26 visualizations, captions communicate the main insight
or takeaway from the visual. Ten of these 26 visualizations belong to A07. An example of a caption describing main takeaway
in a choropleth map (A04) reads: _“[m]any rural counties are do-_
_ing OK”_, followed by a subcaption _“[p]ercentage change in per_
_capita personal income, 2000–2016”_ which explains what data is
displayed on the map. In most of the stories that begin with an _in-_
_teractive_ overview visualization (e.g., A01, A08, A09, B02), the
title of the story also serves as the caption of the first visualization,
thereby serving as a connection between the two media. _Textual an-_
_notations_ are another way of blending textual explanations or labels
in a visualization. They may include data labels—labels of states in
a choropleth map or dots in a scatterplot—(in 45/118 visualizations) or explanations (in 10/118 visualizations). While most of the
annotated points or regions are picked up and explained in the textual narrative, a few stories include longer explanations inside the
visualization (A04, A07, A09). For instance, textual annotations


Almost half (46%) of the visualizations in our collection contain
some variant of a textual annotation. _Tooltips_ are another way of
incorporating short on-demand textual explanations for interactive
visualizations. One choropleth in A11 offers a tooltip that is always
activated, and it gets updated on selection of regions.


Second, _**text-to-vis**_ linking references visualizations as the users
read through the text. Before reporting _insights_, visualizations are
often first introduced in the textual narrative ( _visualization intro-_
_duction_ ). This part of the narrative may include explanation of visual encoding (e.g., _“[t]he red, blue, black and white colors reflect_
_the cheap plastic sheeting available to make shelters at the time”_
– A05) or a certain specificity of a visualization that is not obvious
(e.g., _“map is drawn to maximize the number of districts that usu-_
_ally vote Republican [...]”_ – A06). We observed fewer introductory
sentences for visualizations in Collection B. It may be because visualizations are mostly standard and relate to a rather well-known
COVID-19 data. Visualizations in our collection did not carry iden

318



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_























**Figure 3:** _Flow and structure of stories. Each story is represented by a series of rectangles encoding the type of sentences (heading,_ _**data-**_
_**driven**_ _,_ _**embedding**_ _, and_ _**visualization–text linking**_ _) and_ _**visualizations**_ _. The width of each rectangle encodes the size of a sentence (word_
_count) or a visualization (estimated word count equivalent). White gaps indicate paragraph spacing. Rectangles are vertically (equally)_
_divided in case a sentence has multiple codes assigned to it. The thumbnails on the right show 17 visualizations from our sample collection._



tifiers, so they may not be referenced like in a scientific document
(e.g., _“Figure X”_ ). Instead, they are _cross-referenced_ by the name
of the visualization (e.g., _“see the scatter plot”_ ) or by directional
phrases (e.g., _“the map below“_ ) in case there are multiple visualizations of the same type close by. We observed 36 instances of
named or directional cross-references. We also observed _color-link-_

_ing_ in two stories (A05, A10). Various parts of textual narrative are
formatted (e.g., font colors or colored highlighting) to match and
connect them with visual marks on the visualization. One such ex
ample is shown below (A05):


Hovering over these text blocks highlight the relevant segments
of the charts. The 5 instances of color linking, we observed, were
all interactive.


**5.2. Embedding of Visualizations into the Narration (Q2.2)**


Visualization are embedded at various points in the story. Figure 3
shows the flow (left to right) and the structure of the stories in our
collection. Every rectangle corresponds to either a sentence or a visualization and is scaled according to the space it consumes. To get
a comparable scale for space consumption across both representations, we converted sizes of visualizations (in pixels) to number of
words that would fit in the same space. We use a web browser’s developer tools to inspect the sizes of paragraphs and visualizations.



Dividing the pixels of a paragraph by the word count of that paragraph resulted in pixel density per word. We averaged this pixel
density across all stories resulting in a value of 1 _,_ 469 _._ 57. We computed the word count for each visualization through dividing the
size of the visualization by the average pixel density. This provided
us an estimate to analyze the spatial importance and arrangement
of content across the two media. Since our mapping is a rough
estimate—diverse font styles, editorial guidelines, and story genres were not accounted for—we have only used it to do a coarsegrained analysis and refrained from inferring fine-grained patterns.


The proportion of textual narrative varies from 8% in B03 to
76% in A02 (Figure 3). We classify all stories into three groups according to the varying proportion of text and visualizations. Fourteen stories are _visualization-dominant_ where visualization occupy
more than 60% of the total content. Five stories (A02, A03, A04,
B06, B08) are _text-dominant_ and include more than 60 percent of
textual content. Only three stories (A01, A04, B01) are _balanced_
as they contain textual content in the range of 40–60%.


Figure 3 allows us to study the arrangement and sequence of
content. All stories begin with a title ( _heading_ ) and are mostly (18
of 22) organized in multiple sections as indicated by further _head-_
_ings_ . As we can observe from the blank spaces in Figure 3, which
map to the spacing between paragraphs, most stories also make use
of paragraphs for further text structuring. However, the diversity
is obvious—from no use of sections and paragraphs (except for
text breaks for adding the visualizations) in A11 to a fine-grained
section structuring in A05 and mostly single-sentence paragraphs
in B01.


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



319



Nine out of 22 stories include an _overview_ visualization right below the title to begin with the story. While six (A01, A08, A09,
A12, B02, B07) of these contain a map as an opening visual—A1
and A12 have animated maps—, others include a line plot (B03)
or a small dashboard (B08, containing two stacked bar charts).
Overall, thirteen out of 22 stories have map as their first visualization. _Detail_ and _comparison_ visualizations usually appear after
the overview visualization and are often placed in different sections
of the story following a semantic grouping (A04, A07, B01, B05,
B07, B09, B10). Figure 3 shows few characteristic examples of detail and comparison visualizations for A04, A07, B01, B03, and
B05 along with their positions in the stories.


**6. Study Limitations**


In every empirical study, the sampling of subjects (here, the stories)
can substantially influence the results. We intentionally sampled the
examples from sources of high-quality, both with respect to text
and visualizations. This is not a representative sample of all such
stories but provides a better basis for observing latest trends and
extracting best practices. Besides, 50% (11/22) of the stories were
taken from just two sources New York Times (NYT) and FiveThirtyEight (538). The particular style of their reporting may have biased the results. The limited size of the sample is counterbalanced
by a fine-grained sentence-level analysis of the text and a detailed
classification of the visualizations. The diversity of the examples
in Collection A of the sample is broad, however, it may not fully
cover the possible design space; like every sample taken from realworld examples, it just reflects the space of practices. More than
research prototypes and design studies, these examples might be
limited by technical constraints that need to be considered for their
wide availability (e.g., browser performance, cross-platform compatibility, choice of visualizations).


Another threat to validity is how much we, as authors, might
have biased the results. The authors are from the visualization com
munity and might tentatively overestimate the role of the visual
content presentation. Our motivation to investigate the interplay of
text and visualization might interfere with a neutral and objective
interpretation of this interplay (Q2). In general, assigning codes
is always subjective. We counterbalanced this by partly redundant
coding of two coders and joint discussions of potentially ambiguous and conflicting code assignment.


**7. Study Implications**


While the empirical results reflect the detailed findings that address
the initial research questions, we also want to highlight what can be
learned from this study regarding a broader perspective. This perspective takes into consideration the practical aspects of authoring
visual (geographic) stories and implementing systems to support an
eased creation of such stories.


**7.1. Best Practices of Story Design**


Important lessons from our study are the good practices we observed in the sampled stories. They can provide helpful guidelines
for designers of similar stories and might inspire hypotheses of


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.



follow-up empirical studies. Please note, however, that we are interpreting the above empirical results, condense them beyond a purely
observatory view, and judge which practices we consider as being
positive. Hence, the following practices should not be treated as
empirical findings, but as informed, yet still preliminary suggestions being open for debate within the community.


_Use vernacular geographic language._ Besides precise and exact _location_ identifiers, we observed that the use of vernacular language is common while describing geographic regions (e.g., southern tip of Bangladesh, downtown Los Angeles). Vernacular language helps in abstracting geographic entities beyond regions having clear boundaries and is understood by the target audience. This
aligns with the findings of Hollenstein et al. [HP10] that people use
vernacular terminology to describe locations while tagging images
on the image sharing platform _Flickr_ .


_Summarize common fate._ We observe that results are described
along _clusters_ (Q1.1) to summarize certain joint properties. This
goes beyond just identifying data similarities of any entities and
takes into account geographic or demographic properties that are
not necessarily contained in the data. _Overview_ visualizations
(Q1.2) complement this textual description by showing entities
with similar data values and value changes.


_Different is interesting. Outliers_ and _extrema_ (Q1.1) hint at interesting exceptional cases worthwhile to report. Explicit textual _**com-**_
_**parison**_ —such as _part-to-whole_ comparisons, _correlations_, and
_ranking_ (Q1.1)—specifically contrast two or more entities. Besides,
_comparison_ visualizations (Q1.2) stress noteworthy differences between various entities. Through these means, authors can build an
interesting contrast to the summarized similarities discussed above
or combine the two approaches to, for instance, provide a comparison of clusters.


_Provide sufficient background._ A substantial amount of text in
the stories does not report the data but some form of _background_
that is necessary to understand the data and the story. Also, introducing additional _domain knowledge_ and _dataset descriptions_ can
be helpful. Hence, authors should always consider these categories
to provide sufficient context for the reader to follow.


_Quotes and opinion make it personal._ We have observed many
_quotes_ from experts and politicians, which provide background and
opinion. Further opinion is shared by the authors through _judg-_
_ment_ . While these more subjective views should be clearly discerned from the objective data reporting, such elements can make
the text more personal and interesting for the readers, also receiving
support in forming their own opinion about the subject matter.


_Add text in visualizations. Captions_, _annotations_, and _tooltips_
blend in textual explanations next to or on top of a visualization
(Q2.1, _**text-in-vis**_ ). We observed that 86% (91/118) of the visualizations include captions and, in about 29% (26/91) of the cases,
these captions convey the main takeaway. These kinds of text elements can make the visualization self-explanatory and can hint at
specific insights. Longer explanatory annotations make it possible
to even include non-standard visualization (e.g., Sanky diagrams,
beeswarm plots) in a story. Generally, informative captions can reduce the mental effort to process a data visualization [WAJS21].


320



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



_Describe what you visualize._ In 77% (17/22) of the stories, we
observe that visualizations are explicitly referenced in the text
(Q2.1, _**text-to-vis**_ ). It is important to describe _what_ is visualized
and _how_ it is visualized (e.g., explain non-intuitive encoding), especially if the visualization might not be familiar for every reader ( _vi-_
_sualization introduction_ ). This also contributes toward an improved
linking of the two media. Another, rather less frequent but, interesting way of visualization–text linking is the use of consistent colors
that can make the visualization-related parts of the text stand out.


_Position matters._ Almost all visualizations were placed very
close to the text that describes or references them (Q2.2). The visualization put next to the text helps readers better understand the
descriptions. Besides, it avoids unnecessary scrolling or similar interactions for connecting the visual with text. In one story (A05),
an overview map visualization is placed as a background that keeps
on updating while other detail visualizations and textual content is
blended in on top as the reader scrolls through the story.


_Overview first._ Once more, Shneiderman’s Visual Information
Seeking Mantra seems to apply ( _“Overview first, zoom and filter,_
_then details-on-demand”_ ) [Shn96]. However, here, it does not refer to a sequence of user interactions but can be mapped to the
sequence of visualizations in the story. As discussed for Q2.2., the
first visual representation is often an _overview_ visualization, followed by _detail_ and _comparison_ (a kind of zoomed or filtered representation) visualizations later in the story. Not necessarily the same,
but different _**types**_ of visualizations might best fit these different
purposes (Q1.2).


**7.2. Automatic Report Generation**


Another possible application of our findings relates to the automatic generation of analysis reports. Some efforts have already
been made in this regard, for instance, with respect to weather forecasts [RSBBT15] or bivariate geographic data [LB19a]. These examples usually follow a certain pre-defined structure and are not
yet flexible in telling different stories.


First, the content for presentation needs to be selected. While,
for visualizations, often the raw data can be shown, the textual content requires significant selection and prioritization. Some of the
data-driven findings are easy to compute, such as _extrema_, _clusters_,
and _correlations_ (Q1.1). However, additional background on geography might be necessary to group these entities that form natural
clusters in the eye of a human reader (see discussion on _locations_ ).
Moreover, content prioritization might be necessary because otherwise too many findings will be reported. Regarding the _**context**_ that
the narration provides, _background_ can be filled in with information
from encyclopedias and knowledge graphs. _Quotes_ are harder to select, but still realistic if there exists a collection of quotes that can
be tried to match to a certain finding in the data. However, anything
relating to opinion ( _interpretation_, _judgment_, _conclusion_ ) should be
avoided in an automatic approach—ethical issues might arise if a
machine provides “subjective” data interpretation.


With respect to text generation technologies [GK18] for _**data-**_
_**driven**_ text, template-based approaches can be used but require
larger manual efforts to consider all cases. While machine learning approaches are more flexible but are harder to train and control.



It might be hard to seamlessly interlace data-driven text generated
from the data and text providing _**context**_ as observed for the studied
examples (Q2.2). Hence, an automatic solution might clearly discern between different types of textual explanations, for instance,
_data-driven explanations_, _educational explanations_, and _method-_
_ological explanations_ [MLBW20].


We have observed that multiple visualizations can be combined
into one story where text often serves as glue between the visualizations (Q2.2). For automatic approaches, it might be easier to
focus on visualization-dominated stories (Q2.2) instead of telling
a complex narrative through text. Particularly, _**text-in-vis**_ elements
are easier to generate and mix with existing interactive visualization
approaches. We assume that automated approaches would profit
from interactions to link the text and visualization. For instance,
it would be easier in an automated approach to make every implicit co-referencing link between a text and visualization explicit
by highlighting the linked textual and visual content on hover.


**8. Conclusion**


With this qualitative and fine-grained analysis of geographic datadriven stories, we aimed at getting a deeper understanding of the
interplay of textual narration and visualization. We observed various patterns and relevant examples of how data-driven insights are
reported in the text and how these are embedded with diverse contextual information. Visualizations of different kinds complement
the narration with overview, details, and comparison. The text and
visualizations play together through explicit links like textual annotations of the visualizations and, more implicitly, through data
co-references and placement. Together, they form stories that seamlessly blend textual and visual content. We hope that the identified
best practices will help authors of data stories to follow the stateof-the-art in visual storytelling and can be used for teaching professionals in visual data reporting. Learning from these examples
and results, we also want to inform the design of visual data reporting solutions and story authoring tools. With this, we contribute
to the vision of a widely accessible visual data analysis. We also
believe that the identified qualitative codes are valuable addition.
Going forward, it would be interesting to evaluate the usefulness of
our codes to a larger collection of geographic data stories and even
extend them to include other types of stories.


**Acknowledgments**


We wish to thank Denis Artjuch for his support in collecting,
prepossessing, and coding of the data. We thank the anonymous reviewers for their constructive feedback. The project is
funded by the Deutsche Forschungsgemeinschaft (DFG, German
Research Foundation) – 424960846. The project is also supported
by Shanghai Municipal Science and Technology Major Project
2021SHZDZX0103, 2018SHZDZX01 and ZJLab.


**References**


[AHRL _[∗]_ 17] A MINI F., H ENRY R ICHE N., L EE B., M ONROY H ERNÁNDEZ A., I RANI P.: Authoring data-driven videos with dataclips. _IEEE Transactions on Visualization and Computer Graphics 23_, 1
[(2017), 501–510. doi:10.1109/TVCG.2016.2598647. 2](https://doi.org/10.1109/TVCG.2016.2598647)


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_



321




[BLC20] B ARRAL O., L ALLÉ S., C ONATI C.: Understanding the effectiveness of adaptive guidance for narrative visualization: a gaze-based
analysis. In _Proceedings of the 25th International Conference on In-_
_telligent User Interfaces_ [(2020), pp. 1–9. doi:10.1145/3377325.](https://doi.org/10.1145/3377325.3377517)
[3377517. 2](https://doi.org/10.1145/3377325.3377517)


[BLHR _[∗]_ 19] B REHMER M., L EE B., H ENRY R ICHE N., T ITTSWORTH
D., L YTVYNETS K., E DGE D., W HITE C.: Timeline Storyteller: The
design & deployment of an interactive authoring tool for expressive timeline narratives. In _Proceedings of the Computation + Journalism Sym-_
_posium._ (2019). 2


[BW17] B ECK F., W EISKOPF D.: Word-sized graphics for scientific
texts. _IEEE Transactions on Visualization and Computer Graphics 23_, 6
[(2017), 1576–1587. doi:10.1109/TVCG.2017.2674958. 2](https://doi.org/10.1109/TVCG.2017.2674958)


[BWF _[∗]_ 18] B ACH B., W ANG Z., F ARINELLA M., M URRAY -R UST D.,
H ENRY R ICHE N.: Design patterns for data comics. In _Proceedings_
_of the 2018 CHI Conference on Human Factors in Computing Systems_
[(2018), ACM, pp. 1–12. doi:10.1145/3173574.3173612. 2](https://doi.org/10.1145/3173574.3173612)


[CSC _[∗]_ 21] C HOUDHRY A., S HARMA M., C HUNDURY P., K APLER T.,
G RAY D. W., R AMAKRISHNAN N., E LMQVIST N.: Once upon a time
in visualization: Understanding the use of textual narratives for causality. _IEEE Transactions on Visualization and Computer Graphics 27_, 2
[(2021), 1332–1342. doi:10.1109/TVCG.2020.3030358. 2](https://doi.org/10.1109/TVCG.2020.3030358)


[CZGR09] C HANG R., Z IEMKIEWICZ C., G REEN T. M., R IBARSKY
W.: Defining insight for visual analytics. _IEEE Computer Graphics and_
_Applications 29_ [, 2 (2009), 14–17. doi:10.1109/MCG.2009.22. 3](https://doi.org/10.1109/MCG.2009.22)


[GBWI17] G OFFIN P., B OY J., W ILLETT W., I SENBERG P.: An exploratory study of word-scale graphics in data-rich text documents. _IEEE_
_Transactions on Visualization and Computer Graphics 23_, 10 (2017),
[2275–2287. doi:10.1109/TVCG.2016.2618797. 2](https://doi.org/10.1109/TVCG.2016.2618797)


[GK18] G ATT A., K RAHMER E.: Survey of the state of the art in natural
language generation: Core tasks, applications and evaluation. _Journal_
_of Artificial Intelligence Research 61_ [(2018), 65–170. doi:10.1613/](https://doi.org/10.1613/jair.5477)
[jair.5477. 10](https://doi.org/10.1613/jair.5477)


[HDH _[∗]_ 13] H ULLMAN J., D RUCKER S., H ENRY R ICHE N., L EE B.,
F ISHER D., A DAR E.: A deeper understanding of sequence in narrative
visualization. _IEEE Transactions on Visualization and Computer Graph-_
_ics 19_ [, 12 (2013), 2406–2415. doi:10.1109/TVCG.2013.119. 2,](https://doi.org/10.1109/TVCG.2013.119)
3


[HKL17] H ULLMAN J., K OSARA R., L AM H.: Finding a clear path:
Structuring strategies for visualization sequences. In _Computer Graphics_
_Forum_ [(2017), vol. 36, pp. 365–375. doi:doi.org/10.1111/cgf.](https://doi.org/doi.org/10.1111/cgf.13194)
[13194. 2](https://doi.org/doi.org/10.1111/cgf.13194)


[HP10] H OLLENSTEIN L., P URVES R.: Exploring place through usergenerated content: Using flickr tags to describe city cores. _Journal of_
_Spatial Information Science 2010_ [, 1 (2010), 21–48. doi:10.5311/](https://doi.org/10.5311/JOSIS.2010.1.3)
[JOSIS.2010.1.3. 9](https://doi.org/10.5311/JOSIS.2010.1.3)


[ILQC18] I SENBERG P., L EE B., Q U H., C ORDEIL M.: Immersive visual data stories. In _Immersive Analytics_ . Springer, 2018, pp. 165–184.
2


[KM13] K OSARA R., M ACKINLAY J.: Storytelling: The next step for
visualization. _Computer 46_ [, 5 (2013), 44–50. doi:10.1109/MC.](https://doi.org/10.1109/MC.2013.36)
[2013.36. 2](https://doi.org/10.1109/MC.2013.36)


[LB18] L ATIF S., B ECK F.: Visually augmenting documents with data.
_Computing in Science Engineering 20_, 6 (2018), 96–103. [doi:10.](https://doi.org/10.1109/MCSE.2018.2875316)
[1109/MCSE.2018.2875316. 2](https://doi.org/10.1109/MCSE.2018.2875316)


[LB19a] L ATIF S., B ECK F.: Interactive map reports summarizing bivariate geographic data. _Visual Informatics 3_, 1 (2019), 27–37. Proceedings
[of PacificVAST 2019. doi:10.1016/j.visinf.2019.03.004.](https://doi.org/10.1016/j.visinf.2019.03.004)
10


[LB19b] L ATIF S., B ECK F.: VIS Author Profiles: Interactive descriptions of publication records combining text and visualization. _IEEE_
_Transactions on Visualization and Computer Graphics 25_, 1 (2019),
[152–161. doi:10.1109/TVCG.2018.2865022. 2](https://doi.org/10.1109/TVCG.2018.2865022)


_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.




[LTW _[∗]_ 18] L IU Z., T HOMPSON J., W ILSON A., D ONTCHEVA M., D E LOREY J., G RIGG S., K ERR B., S TASKO J.: Data Illustrator: Augmenting vector design tools with lazy data binding for expressive visualization authoring. In _Proceedings of the 2018 CHI Conference on_
_Human Factors in Computing Systems_ (2018), ACM, pp. 123:1–123:13.
[doi:10.1145/3173574.3173697. 2](https://doi.org/10.1145/3173574.3173697)


[MHRL _[∗]_ 17] M C K ENNA S., H ENRY R ICHE N., L EE B., B OY J.,
M EYER M.: Visual narrative flow: Exploring factors shaping data visualization story reading experiences. In _Computer Graphics Forum_ (2017),
vol. 36, Wiley Online Library, pp. 377–387. 2, 3


[MLBW20] M UMTAZ H., L ATIF S., B ECK F., W EISKOPF D.: Exploranative code quality documents. _IEEE Transactions on Visualization_
_and Computer Graphics 26_ [, 1 (2020), 1129–1139. doi:10.1109/](https://doi.org/10.1109/TVCG.2019.2934669)
[TVCG.2019.2934669. 2, 10](https://doi.org/10.1109/TVCG.2019.2934669)


[MZJS18] M ETOYER R., Z HI Q., J ANCZUK B., S CHEIRER W.: Coupling story to visualization: Using textual analysis as a bridge between
data and interpretation. In _23rd International Conference on Intel-_
_ligent User Interfaces_ (2018), ACM, p. 503–507. [doi:10.1145/](https://doi.org/10.1145/3172944.3173007)
[3172944.3173007. 2](https://doi.org/10.1145/3172944.3173007)


[Nor06] N ORTH C.: Toward measuring visualization insight. _IEEE Com-_
_puter Graphics and Applications 26_ [, 3 (2006), 6–9. doi:10.1109/](https://doi.org/10.1109/MCG.2006.70)
[MCG.2006.70. 3](https://doi.org/10.1109/MCG.2006.70)


[OKCP19] O TTLEY A., K ASZOWSKA A., C ROUSER R. J., P ECK E. M.:
The Curious Case of Combining Text and Visualization. In _EuroVis 2019_

_- Short Papers_ [(2019), The Eurographics Association. doi:10.2312/](https://doi.org/10.2312/evs.20191181)
[evs.20191181. 1, 2](https://doi.org/10.2312/evs.20191181)


[RBL _[∗]_ 17] R EN D., B REHMER M., L EE B., H ÖLLERER T., C HOE
E. K.: ChartAccent: Annotation for data-driven storytelling. In _2017_
_IEEE Pacific Visualization Symposium_ (2017), pp. 230–239. [doi:](https://doi.org/10.1109/PACIFICVIS.2017.8031599)
[10.1109/PACIFICVIS.2017.8031599. 2](https://doi.org/10.1109/PACIFICVIS.2017.8031599)


[RHDC18] R ICHE N. H., H URTER C., D IAKOPOULOS N., C ARPEN DALE S.: _Data-driven storytelling_ . CRC Press, 2018. 2


[RSBBT15] R AMOS -S OTO A., B UGARIN A. J., B ARRO S., T ABOADA
J.: Linguistic descriptions for automatic generation of textual shortterm weather forecasts on real prediction data. _IEEE Transactions on_
_Fuzzy Systems 23_ [, 1 (2015), 44–57. doi:10.1109/TFUZZ.2014.](https://doi.org/10.1109/TFUZZ.2014.2328011)
[2328011. 10](https://doi.org/10.1109/TFUZZ.2014.2328011)


[SH10] S EGEL E., H EER J.: Narrative visualization: Telling stories with
data. _IEEE Transactions on Visualizations and Computer Graphics 16_,
[6 (2010), 1139–1148. doi:10.1109/TVCG.2010.179. 1, 2, 3](https://doi.org/10.1109/TVCG.2010.179)


[Shn96] S HNEIDERMAN B.: The eyes have it: A task by data type
taxonomy for information visualizations. In _Proceedings of the 1996_
_IEEE Symposium on Visual Languages_ (1996), IEEE Computer Society,
[pp. 336–343. doi:10.1109/VL.1996.545307. 10](https://doi.org/10.1109/VL.1996.545307)


[SND05] S ARAIYA P., N ORTH C., D UCA K.: An insight-based methodology for evaluating bioinformatics visualizations. _IEEE Transactions_
_on Visualization and Computer Graphics 11_ [, 4 (2005), 443–456. doi:](https://doi.org/10.1109/TVCG.2005.53)
[10.1109/TVCG.2005.53. 3](https://doi.org/10.1109/TVCG.2005.53)


[SXS _[∗]_ 21] S HI D., X U X., S UN F., S HI Y., C AO N.: Calliope: Automatic
visual data story generation from a spreadsheet. _IEEE Transactions on_
_Visualization and Computer Graphics 27_ [, 2 (2021), 453–463. doi:10.](https://doi.org/10.1109/TVCG.2020.3030403)
[1109/TVCG.2020.3030403. 2](https://doi.org/10.1109/TVCG.2020.3030403)


[TRB _[∗]_ 18] T ONG C., R OBERTS R., B ORGO R., W ALTON S., L ARAMEE
R. S., W EGBA K., L U A., W ANG Y., Q U H., L UO Q., ET AL .: Storytelling and visualization: An extended survey. _Information 9_, 3 (2018),
[65. doi:10.3390/info9030065. 2](https://doi.org/10.3390/info9030065)


[WAJS21] W ANZER D. L., A ZZAM T., J ONES N. D., S KOUSEN D.: The
role of titles in enhancing data visualization. _Evaluation and Program_
_Planning 84_ [(2021), 101896. doi:10.1016/j.evalprogplan.](https://doi.org/10.1016/j.evalprogplan.2020.101896)
[2020.101896. 9](https://doi.org/10.1016/j.evalprogplan.2020.101896)


[WSZ _[∗]_ 19] W ANG Y., S UN Z., Z HANG H., C UI W., X U K., M A X.,
Z HANG D.: Datashot: Automatic generation of fact sheets from tabular
data. _IEEE Transactions on Visualization and Computer Graphics 26_, 1
[(2019), 895–905. doi:10.1109/TVCG.2019.2934398. 2](https://doi.org/10.1109/TVCG.2019.2934398)


322



_S. Latif, S. Chen, & F. Beck / Visualization–Text Interplay in Geographic Data-driven Stories_




[ZOM19] Z HI Q., O TTLEY A., M ETOYER R.: Linking and layout: Exploring the integration of text and visualization in storytelling. In _Com-_
_puter Graphics Forum_ [(2019), vol. 38, pp. 675–685. doi:10.1111/](https://doi.org/10.1111/cgf.13719)
[cgf.13719. 1, 2](https://doi.org/10.1111/cgf.13719)



_⃝_ c 2021 The Author(s)
Computer Graphics Forum c _⃝_ 2021 The Eurographics Association and John Wiley & Sons Ltd.


