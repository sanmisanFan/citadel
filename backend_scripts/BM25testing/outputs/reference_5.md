IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011



2231


# Visualization Rhetoric: Framing Effects in Narrative Visualization

Jessica Hullman, _Student Member, IEEE,_ and Nicholas Diakopoulos, _Member, IEEE_

**Abstract** —Narrative visualizations combine conventions of communicative and exploratory information visualization to convey an
intended story. We demonstrate _visualization rhetoric_ as an analytical framework for understanding how design techniques that
prioritize particular interpretations in visualizations that “tell a story” can significantly affect end-user interpretation. We draw a
parallel between narrative visualization interpretation and evidence from framing studies in political messaging, decision-making,
and literary studies. Devices for understanding the rhetorical nature of narrative information visualizations are presented, informed
by the rigorous application of concepts from critical theory, semiotics, journalism, and political theory. We draw attention to how
design tactics represent additions or omissions of information at various levels—the data, visual representation, textual annotations,
and interactivity—and how visualizations denote and connote phenomena with reference to unstated viewing conventions and
codes. Classes of rhetorical techniques identified via a systematic analysis of recent narrative visualizations are presented, and
characterized according to their rhetorical contribution to the visualization. We describe how designers and researchers can benefit
from the potentially positive aspects of visualization rhetoric in designing engaging, layered narrative visualizations and how our
framework can shed light on how a visualization design prioritizes specific interpretations. We identify areas where future inquiry
into visualization rhetoric can improve understanding of visualization interpretation.


**Index Terms** —Rhetoric, narrative visualization, framing effects, semiotics, denotation, connotation.


**1** **I** **NTRODUCTION**



Narrative information visualizations are a style of visualization that
often explores the interplay between aspects of both explorative and
communicative visualization [38]. They typically rely on a
combination of persuasive, rhetorical techniques to convey an
intended story to users as well as exploratory, dialectic strategies
aimed at providing the user with control over the insights she gains
from interaction. Segel and Heer take an initial step towards
highlighting how varying degrees of authorial intention and user
interaction are achieved by general design components in narrative
visualization [38]. This blend of explorative and communicative
features presents another research opportunity though: to better
understand a user’s interpretation process of a narrative visualization
in light of the rhetorical conventions that the author employs. By
_explicating_ _rhetorical techniques and how such techniques may_
_affect user interpretation_, researchers and designers alike stand to
gain a tool for understanding how visualizations communicate.
In this work we examine the design and end-user interpretation of
narrative visualizations in order to deepen understanding of how
common design techniques represent rhetorical strategies that make
certain interpretations more probable. How are rhetorical techniques
used in visualization and what are the effects of these techniques on
user interpretations of data? Studies in semiotics, journalism, and
critical theory indicate particular rhetorical techniques used to
communicate an intended message [1, 2, 23]. while evidence from
decision theory, survey design, and political theory [21, 36, 37]
suggests that subtle variations in a representation’s rhetorical or
persuasive techniques can generate large effects on users’
interpretations of a message. Investigations related to InfoVis
provide initial evidence that how data is framed or presented can
significantly affect interpretation [3].
Given the motivation to better understand the interpretation
process of visualization, this paper investigates rhetorical strategies
and effects in narrative visualization by addressing the following
research questions:


- _Jessica Hullman is with the University of Michigan, jhullman@umich.edu._

- _Nicholas Diakopoulos is with Rutgers University,_
_nicholas.diakopoulos@gmail.com._


_Manuscript received 31 March 2011; accepted 1 August 2011; posted online_
_23 October 2011; mailed on 14 October 2011._
_For information on obtaining reprints of this article, please send_
_email to: tvcg@computer.org._




- What particular conventions are used, and to what extent are
specific techniques associated with different editorial layers in
the visualization (such as the data, visual representation,
annotation, and interactivity)?

- In what ways can factors external to the visualization itself,
such as internalized knowledge and conventions at the
individual and community level, interact with the rhetorical
strategies used in a narrative visualization to influence
interpretation?

- How do communicative and explorative rhetorical strategies
effectively work together in a narrative visualization?
This work contributes to InfoVis design and theory by providing
insight into (1) the types and forms of use of particular rhetorical
techniques in narrative visualizations, and (2) the interaction between
those techniques and individual and community characteristics of
end-users. The first contribution is a taxonomy of how particular
design elements can be used strategically to directly or indirectly
prioritize certain interpretations. This equips designers with a set of
techniques for designing engaging narrative visualizations capable of
communicating layered meanings. At the same time, the
identification of classes of rhetorical techniques provides both
designers and InfoVis researchers with a vocabulary for analyzing
the underlying rhetorical functions of particular design strategies, a
dimension that remains under-discussed in many theoretical
frameworks organized primarily around exploratory visualization.
The second contribution of this work is in identifying and
demonstrating how these conventions interact with characteristics of
the visualization interaction, end-user’s knowledge, and the sociocultural context. This stands to improve designers’ awareness of how
designs might be received differently by individual end-users and
how they can cue shared cultural knowledge and associations. These
“extra-representational” factors also tend to be neglected when
designing or analyzing visualizations based on design principles such
as those proposed by Tufte [45]. Researchers in InfoVis can benefit
from a holistic understanding of visualization interpretation capable
of providing insight into how particular interpretations arise as a
result of interactions between a visualization, user mental models,
and other external representations. This view is congruent with a
distributed cognition model of InfoVis [26].
This paper is organized as follows: Section 2 defines important
terms related to rhetoric and contextualizes these concepts in InfoVis
as well as semiotics, decision science, and political theory. We also
describe our work in the context of research on narrative



1077-2626/11/$26.00 © 2011 IEEE    Published by the IEEE Computer Society


2232 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011



visualization. Section 3 outlines many specific visualization rhetoric
techniques based on a systematic qualitative analysis of narrative
visualizations, and describes how these techniques form clusters of
strategies exemplifying different rhetorical operations. Analytical
devices for understanding the site of techniques and their interaction
with end-user characteristics are also presented. Section 4 uses two
case studies to demonstrate how an understanding of visualization
rhetoric can provide insight for the analysis and design of narrative
visualizations. Section 5 discusses themes emerging from our
analyses and highlights areas for future study.


**2** **B** **IAS AND** **R** **HETORIC IN** **C** **OMMUNICATION**


In this section we address the terminology used in the paper and
define visualization rhetoric. We then motivate the importance of our
work and contextualize it with that of other relevant fields. This

draws attention to the need for deeper understanding of visualization
interpretation as it relates to rhetorical techniques and design.


**2.1** **A Note on Nomenclature**

This paper’s focus on visualization rhetoric stands at the intersection
of ideas of _bias_ and user-designer relationships as understood in
InfoVis, on the one hand, and theories of _rhetoric, framing_ and
author-reader interactions as elaborated in critical semiotic theories
for literature, political rhetoric, and media artifacts on the other.
_Bias_, _rhetoric, framing_ (and the related literary term _perspective_ ) all
describe how an interpretation arises from the interaction of
representational, individual, and social forces. Differences can be
traced mostly to superficial differences adhering in ordinary
language. _Bias_ is often defined in negatively connoted terms: “a
systematic error introduced into sampling or testing by selecting or
encouraging one outcome or answer over others” [MerriamWebster]. To _frame_ an idea is typically more neutrally defined as to
“form or articulate” [Oxford American] or “shape, construct”

[Merriam-Webster]. Similarly, the concept of perspective tends to be
either neutrally or positively-connoted in literary and critical theory
as a productive force in the telling of a story. The term _rhetoric_ has a
complex history, but has come to be associated with persuasion as a
result of the implicit motivation of the speaker to gain other
adherents to a preconceived view or conclusion [7].
We use the term rhetoric to refer to the set of processes by which
intended meanings are represented in the visualization via a
designer’s choices and then shaped by individual end-user
characteristics, contextual factors involving societal or cultural
codes, and the end-user’s interaction. While this term may bring to
mind negatively connoted notions of persuasion as bias common in
some InfoVis literature, we seek to objectively describe the
rhetorical nature of visualization design rather than to comment on
the appropriateness of persuasion in visualization design.


**2.2** **Information Visualization**

Despite its parallel meaning to terms like _rhetoric_, the pejorative
term _bias_ is more often found in InfoVis literature. Early theory
emphasizes the analytic nature of graphical displays (e.g. [8]), as
well as automated methods that optimize constraints imposed by
human perceptual and cognitive abilities (e.g. [27]). Unequivocal
designs are prioritized; “in the ideal case a chart or graph will be
absolutely unambiguous, with its intended interpretation being
transparent” ([22], pg. 192). Immediate clarity and minimal
intervention on the part of the creator are emphasized [45]. Where
editorial choices must be made, designers are urged to provide
detailed provenance information like the objective, time, and
location of graph creation [44].
Some recent InfoVis work has striven to overcome the narrow
focus on optimizing visualization clarity and efficiency that
dominated earlier work, acknowledging that interacting with a
visualization involves thinking about and being influenced by factors
beyond just the visual representation. Evaluation models like [30]
explicitly acknowledge that risks to validity can enter at levels



beyond the visual encoding and interaction design, such as in
characterizing the domain tasks and data. Additionally, several
studies demonstrate that extra-representational preferences and
conventions can influence interpretation, such as when the visual
format cues interpretation frames [3] or individual differences lead to
differing visualization usage [56]. As Norman [32] describes,
interpretations can be unpredictable when design elements may not
immediately communicate the designer’s intended meaning as a
result of influences on interpretation deriving from the end-user’s
context. Liu and Stasko [26] frame the site of such differences via
the mental model concept, arguing that the effects of such
differences on interpretation have been underexplored in InfoVis.
This supports a call for further consideration of visualization’s role
within webs of situated representations.
The visualization rhetoric model we propose is likewise
motivated by an expanded view of visualization that takes into
consideration under-acknowledged facets of design and
interpretation. For instance, creating a visual representation
necessitates simplification, as data is used to create an analytical
abstraction that is transformed to a visual representation [55]. Thus a
rhetorical dimension is present in any design. Secondly, a designer’s
intentions may remain implicit and inarticulable by him or her,
making it impossible to comply with the principle of providing full
provenance. From the end-user’s perspective, the pleasure of a
concise, visual representation may be decreased if engaging with the
visualization also requires sifting through explicit description of
every design manipulation.


**2.3** **Framing in Decision and Opinion Formation**

Empirical studies in decision theory and political messaging provide
additional evidence that even subtle changes in the rhetorical frame
of an information presentation can significantly influence responses.
In contrast to the mostly aloof posture towards intentional use of
rhetorical devices in InfoVis literature, psychological, political and
communication theorists have developed framing theory to
investigate opinion formation processes in light of how people orient
their thinking about an issue. Typically, these processes are viewed
as responses to the use of particular communicative structures in
messaging (e.g., [12, 21, 46]). Researchers seek to better understand
“framing effects”, situations where often small changes in the
presentation of an issue or an event, such as slight modifications of
phrasing, produce measurable changes of opinion [35]. Information
representations can influence interpretation in diverse ways, such as
by presenting a preliminary statistic before a decision [ibid], or by
manipulating the anchor points on a survey scale [37]. Of particular
relevance to InfoVis are findings that are explicitly visually-based.
For example, the amount of space provided between response
choices in a scale can be interpreted as reflecting the underlying
dimension and lead to different results when manipulated [43]. This
literature further motivates a need to articulate and understand the
implications of rhetorical strategies in visualization.


**2.4** **Semiotics**

Semiotics describes literary, visual, political, and other critical
studies that examine how representations like texts, paintings,
iconography, or media messaging can be decomposed into systems
of signs. Signs—(defined as any material thing that stands for a nonpresent meaning, such as a word, color choice, or visual icon)—
become meaningful through their interaction with other signs within
a representation, as well as with signs that are culturally present (e.g.,

[2]). Semiotic theory has been introduced in HCI as an inspection
method for interactive interfaces to help assess the designer-user
meta-communication via the interactive artifact [17]. First applied by
Jacques Bertin [4] as a tool for describing how information
visualizations convey meaning, semiotic theories emphasize the
communicative properties of visualizations alluded to in recent
works [48]. This can serve designers seeking to better convey their
intended messages [1] and increase their awareness of how design


HULLMAN AND DIAKOPOULOS: VISUALIZATION RHETORIC: FRAMING EFFECTS IN NARRATIVE VISUALIZATION 2233



choices may affect interpretation. Semiotic theorists analyze the
relationships between forms of media, their production, and the
“modes of seeing” or interpretive conventions that they engender.
The concept of viewing codes, including visual, textual, cultural, and
perceptual [10], describes the implicit, often internalized standards
that support interpreting an artifact in a certain way. This motivates
incorporating extra-representational factors like individual and group
conventions into a visualization rhetoric framework.


**2.5** **Narrative Visualization**

In response to the growing number of online visualizations designed
to convey a story, Segel and Heer’s [38] design space analysis
presents three ways of distinguishing categories of narrative
visualizations: (1) genres; (2) visual narrative tactics that direct
attention, guide view transitions, and orient the user; and (3)
narrative structure tactics such as ordering, interactivity, and
messaging. Their contribution of abstract structures and genres
provides a general framework that opens the discussion of narrative
visualization to a wider range of examples. The framework also
allows comparisons between visualizations based on how they
structure users’ interactions with data. We aim to expand the
discussion of narrative visualizations to include the role of extrarepresentational influencers like individual, group, and contextual
differences in interpretation. We outline additional visual and nonvisual tactics used in narrative visualization, emphasizing how these
represent omissions, additions, and implications.
Ziemkiewicz and Kosara [55] contrast information visualization
with visual representations. Narrative visualizations tend to be
excluded from their model by criteria like non-trivial interactivity
(allowing users to change the visual mapping parameters themselves)
or non one-to-one mappings between the source domain and the
visual output domain. In contrast, our work explores the dynamics of
constrained interactivity and techniques like visual redundancy that
are used to emphasize an intended meaning in narrative
visualization. We also extend their discussion of information loss by
considering the rhetorical effects of information omissions regardless
of intention, based on our belief that the increased presence of such
visualizations makes it important for InfoVis researchers and
practitioners to better understand how the editorial process of
visualizing data necessarily constrains possible interpretations.


**3** **V** **ISUALIZATION** **R** **HETORIC** **F** **RAMEWORK**


A primary contribution of this paper is the development and
demonstration of an analytical framework to guide discussion of the
rhetorical aspects of InfoVis. In this section we present conceptual
devices as well as the results of a large qualitative analysis used to
identify specific rhetorical strategies used in InfoVis. We begin by
describing the _editorial layers_ of a visualization presentation where
rhetorical choices are made, then describe the particular _visualization_
_rhetoric techniques_ identified in our analysis. A discussion of
_viewing codes_ follows, including aspects of _denotation_ and
_connotation,_ which helps capture the role of end-users’ implicit
beliefs and knowledge in visualization interpretation.


**3.1** **Editorial Layers**

Editorial judgments, and thus rhetorical techniques, can enter into the
construction of narrative visualizations from multiple paths. We
distinguish between four **editorial layers** that can be used to convey
meaning, including the data, visual representation, textual
annotations, and interactivity. A given rhetorical technique might be
applied to some layers more easily than others. Yet omissions,
emphases, and ambiguity can be accomplished at each level. As the
output of a designer’s decision processes, a narrative visualization
represents a sequence of choices to either add information (such as
by adding suggestions of an intended message using textual
annotations) or omit information (such as by omitting some variables
or interactivity features). Distinguishing the possible sites of these



choices paves the way for more recognition of their existence, and
effects on end-user interpretations.
At the lowest level of the **data**, the creator of a visualization
makes choices about the data source to represent, including what
variables to include and which to leave out. Additional choices can
further affect data, such as removing outliers, scaling, or aggregating
values. Both of these particular data choices lead to loss of
information in the final representation, yet are necessary choices in
the act of visualization design (see 3.2.2 below). The **visual**
**representation** layer carries traces of choices made about how the
data will be mapped to the visual domain. Often, this mapping is
lossy as a result of human visual perception abilities. For example,
mapping a continuous variable to a gray scale leads to “lost”
information due to human perception’s sensitivity and capability to
distinguish different intensity levels (e.g., “just noticeable
differences”). **Annotations** can be textual, graphical, or social, as in
the inclusion of user comments in the overall presentation.
Annotations have often been overlooked in InfoVis evaluation, yet
serve an important role in many presentations that include
visualization by focusing a user’s attention on specific areas in a
graph. Finally, the **interactivity** of the visualization can be the site of
choices that constrain a user’s interaction in ways that lead her to
explore certain subsets of data. This can occur through navigation
menus that limit the number of views of the data set that are possible,
or linked search suggestions that likewise encourage the user to
explore particular views over others. .


**3.2** **Visualization Rhetoric Techniques**

We describe and present findings on the rhetorical strategies we
observed in an extensive analysis of online narrative visualizations.


3.2.1 Method

We gathered a sample of fifty-one professionally-produced narrative
visualizations, many from international news outlets like the New
York Times (NYT) or BBC. In the interest of diversity we also
included online visualizations from news magazines (e.g. The
Economist); local news providers (e.g. annarbor.com.); political
outlets (e.g. Obama.org, website of the speaker of the house); and
independent graphic designers known to publish their work in
leading news outlets (e.g. David McCandless). Prior to coding, we
familiarized ourselves with framing or bias techniques identified in
semiotics (e.g., [2, 4, 10, 17]), statistical presentation (e.g., [20, 45]).
decision theory (e.g., [12, 21, 46]) and media and communication
studies (e.g., [31]). We iteratively coded particular techniques we
observed referring to this set of theories as a guide, and relied on
general knowledge of current events and how to interpret various
graph formats as needed. We restricted our analysis to the details
present in the visualization and their surrounding presentation. The
saliency and primacy of the observed techniques were considered as
the examples were coded. As coding progressed, we noted where
techniques appeared to represent different implementations of the
same basic function (e.g. thresholding data by removing values
above or below predefined points). In such cases we labelled these
“families” of similar techniques based on their simplest shared trait.
The output of this analysis was a list of visualizations coded for each
technique that appeared.
Affinity diagramming was then used to arrive at higher-level
clusters of techniques. As in the case of creating families of lowlevel techniques, we decided against a formal, mutually-exclusive
scheme in favor of groupings based on similarities in the underlying
mechanism. This strategy was chosen primarily because it yielded
four distinguishable categories that we felt best covered our critical
observations: information access rhetoric functioning to limit the
amount of information presented, provenance rhetoric functioning to
provide background information, mapping rhetoric functioning to
map elements of the visualization to non-explicit concepts, and
procedural rhetoric functioning to constrain interaction over time
(Sections 3.2.2-3.2.4 and 3.2.6). One remaining cluster of techniques


2234 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011


Fig. 1. 'How the Recession Changed Us' (excerpt) by Lavin of _The_
_Atlantic_ [25]. Fig. 2. ʻVehicle Salesʼ by _The Economist_ Daily Chart column [47].



was not clearly distinguishable based on a common mechanism, but
was rather comprised of methods that instead appeared to cluster
based on an origin in linguistic rhetoric (3.2.5). We then tabulated
patterns of frequency and co-occurrence of techniques in order to
show the interrelatedness of the categories (Section 3.2.7).
Alternative schemes of rhetorical techniques may be possible for
narrative visualizations. However, the representativeness of our
sample leads us to believe that the categories below can serve as a
guide for designers seeking to strengthen or subdue rhetorical
effects.


3.2.2 Information Access Rhetoric

The first decisions made by a visualization designer often concern
what data to represent. To simplify complex ideas in a visual
representation it is often helpful to keep distracting or irrelevant
information to a minimum (e.g. [28]). **Omission** techniques are the
least likely to be explicitly indicated by a visualization, yet can be
inferred from data that are available given ample contextual
information. Assuming that most professional producers of online
visualizations are aware of the importance of data provenance,
_neglecting to cite data sources_ or other important provenance
information or _defining variables ambiguously_ can be considered
omissions. These may be motivated by _knowledge assumptions_ of
the end-user, such as when a complex statement is made without
explicit reference to intermediate clauses. In _The Atlantic’s_ ‘How the
Recession Changed Us’ (Fig. 1), the overall message about negative
effects of the recession assumes that end-users intuit several nonexplicit propositions in decoding the iconography and statistics. The
number of times that the word ‘uncertainty’ appeared in the New
York Times, for example, only makes sense in the graphic if one
assumes that mentions of uncertainty in articles equates to economicrelated risks and recession. Omissions may also result from a desire
to simplify complex phenomena by excluding complicating
information from the visual representation, as in the case of
_thresholding values_ or _omitting exceptional cases_ . A visual
representation occurs in _axis thresholding,_ in which the values most
important to communicate a pattern through comparison are used to
set the range of the axis, so that higher or lower values that may be
relevant but complicate the message are not shown.
Omission or information loss choices can also be transferred to
the end-user via _filtering_ capabilities like search bars that allow a
user to select a subset of data. Intentional information loss has been
discussed on the part of the designer [45, 55], but has been
underexplored from the perspective of user-driven filtering. The
increasing prevalence of narrative visualization suggests that userdriven information loss or avoidance may be a fruitful area for
research.
**Metonymy** techniques that manipulate part-whole relationships
serve simplification as well. At the basest level, the _selection of_



_variables_ to visualize involves creating a subset of a larger data set to
present a simplified visual representation of chosen features.
_Averaging_ techniques like mean, median, and clustering similarly
substitute simpler representations for a wider range of values, as do
_textual and visual summaries._ _Categorizing, binning,_ or _aggregating_
values can be used to make an intended effect more apparent. An
Economist graph on car sales [47] (Fig. 2) depicts only ‘light
vehicles’ for some countries’ data, yet all sales for other countries.


3.2.3 Provenance Rhetoric

Similar to objectivity values in InfoVis, journalistic codes of ethics
emphasize the journalist’s duty to remain impartial and present
information as clearly as possible [23]. A number of visualization
rhetoric techniques observed in our sample work to signal the
transparency and trustworthiness of the presentation source to endusers. Doing so conveys a respect for the audience and reaffirms a
journalist’s public interest motive, strengthening the journalist’s
credibility [ibid]. **Data provenance** strategies include _citing and/or_
_linking data sources, additional references, methodological choices_,
and _relevant facts_, as well as _annotating exceptions and corrections,_
thus achieving goals proposed by Tufte for graph provenance [44] _._
Several of these methods are depicted in Fig. 2.
**Representing uncertainty** can be accomplished through visual
representations like _error bars,_ yet appeared more often in our
sample via textual means. These included _descriptions of inferential_
_limits_ (i.e. confidence intervals), _“leap-of-faith” or forecast_
_annotations_ explicitly labelling the point in a graph where data are
extrapolated, or _expressions of doubt_ regarding potential conclusions
(see Fig. 2, tag line below title). The dominance of textual
uncertainty representations suggests an intriguing comparison
between these visualizations and the visually-based ways of denoting
uncertainty that have been developed in InfoVis and statistical
graphics, such as error bars or confidence envelopes (e.g. [50]). The
reliance on textual means may indicate a lack of adequate methods or
commonly understood codes for visually representing uncertainty to
non-experts [39].
Finally, in some cases explicit steps are taken to signal the
**identification** of a visualization’s designer. While author-designers
are usually credited for their work, in some cases additional
information is provided, through _author bios_ or _personal anecdotes._


3.2.4 Mapping Rhetoric

Mapping rhetoric refers to manipulating the information presentation
via the data-to-visual transfer function, the constraints that determine
how a piece of information will be translated to a visual feature.
**Obscuring** can result from introducing “noise” into a representation,
often on a perceptual level, such as in the case of adding a _gratuitous_
_third dimension_ . Other means of obscuring are applications of nonessential _sizing transformations_ that violate _discriminability limits._


HULLMAN AND DIAKOPOULOS: VISUALIZATION RHETORIC: FRAMING EFFECTS IN NARRATIVE VISUALIZATION 2235


Fig. 4. ʻA Peek into Netflix Queuesʼ by Bloch et al. of the NYT [5].



Fig. 3. Chart released on Speaker of the House John Boehnerʼs
website [33] (top); chart in response to same sourceʼs
ʻOrganizational Chart of the Democratʼs Health Planʼ by graphic
designer Robert Palmer [34] (bottom).


This may mean making some elements too small for judgment,
_oversizing_ to the point of overwhelming the presentation, or
obscuring a value’s true position on an axis. More subtly, nonintentional obscuring occurs when a designer _neglects to map_
_information to the most salient visual judgment types_ as suggested by
work like [13]. Noise can be introduced on a semantic level, by
implying _false cause-and-effect_ relationships or by using complex
design tactics like the _double-axis,_ which experts have noted are
difficult to decode even when properly used [50], (see Fig. 2
‘Vehicle Sales’ [47] and Fig. 7 ‘Poll Dancing’ [29]).
**Visual metaphor and metonymy** maps visual signs to nonpresent or implicit meanings. Some of these are interpreted
automatically due to congruence with embodied experience, such as
_suggestive spatial mappings_ like “left = past, right = future” or “up =
more or better, down = less or bad” [24]. _Typographic mappings_ and
_color mappings_ pair visualized patterns to categories via
visualization components, such as by applying red and blue font
colors representing political parties to statistics in an election-themed
visualization [52]. _Visual noise_ is a visual metaphor technique that
can also serve to obscure. It has become popular in recent years
through visualizations like the visually confusing graphics by
political party representatives of political parties to represent the
“confused” policies of the opposing group (see Fig. 3, top). Visual
noise can be used more subtly as well, as in David McCandless’
‘Poll Dancing’ visualization [29] (Fig. 7, below) or more obviously



as in the ‘Organizational Chart of the Democrats’ Health Plan’ [33]
(Fig. 3, top), which prompted a response graph that appeared to be
motivated in part by the goal of creating a distinctly non-noisy graph

[34] (Fig. 3, bottom).
**Contrast** techniques can serve ambiguity, as in the juxtaposition
of oppositional pieces of information that occur in _visual contrasts_ or
_variable splices._ In these cases, information that is not obviously
associated with target variables is included, adding an additional
layer of perspective on an issue. An example can be found in the
NYT interactive visualization entitled ‘A Peek Into Netflix Queues’

[5] (Fig. 4). The title and two variables of rental lists and movie rank
variables are mapped to the important visual dimensions of spatial
position and color. These mappings imply an overall message
organized around geographic patterns in top rentals. However, a
choice was made to include the less obviously relevant critic metascores for each movie, along with a sample NYT review of each, to
the left of the map frame. The result is an implication that this
information may generate further insight through comparisons with
the geographic patterns. Scanning comments attached to the
visualization validates that such comparisons did occur among users.
**Classification** can be accomplished through _grouping by size,_
_position, or color_ (see Fig. 3, bottom) _. Consistent typographic_
_manipulations_ of font sizes and styles and _equations of significance_
presented in a legend-like format to highlight certain values can also
classify information within a visualization. Such classifications can
show clusters of priority or importance.
**Redundancy** techniques emphasize by _disaggregating_
_homogenous values or visual marks._ The repetition of identical
labels, or the disaggregation of values with little variance or similar
functions or relationships between them, can be used both to
emphasize as well as to create _visual noise_ . In a second politicallythemed graph from John Boehner’s office on a new energy tax plan

[41], a label of ‘Higher prices’ is used repeatedly in labels placed
closed to one another, presumably to emphasize the economic
ramifications of the plan on taxpayers over combining the labels into
one. We note that the bijective or one-to-one mapping from the data
to the target (visual) domain required in Ziemkiewicz and Kosara’s
taxonomy for information visualization [55] is violated in nearly all
occurrences of redundancy.


3.2.5 Linguistic-based Rhetoric

Multiple techniques closely resembled rhetorical devices that derive
from conventions of language usage. These techniques tended to be
(but were not exclusively) implemented at the textual layer, albeit
with several exceptions. **Typographic emphases** like font _bolding_
or _italicizing_ derives meaning from conventions long associated with
typography.
**Irony** is a basic literary and artistic strategy that sets up a
discordance between the literal meanings of a statement and an
alternative implied meaning. Visualizations in our sample often used
_rhetorical questions_ with irony, which has an effect of engaging the


2236 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011



user’s attention by directly addressing her, while at the same time
using the question in order to imply its inverse. These tend to be used
in titles to sarcastically set the stage for a user to arrive at an obvious
interpretation, as in ‘Budget Forecasts, Compared With Reality’ [16]
where a prominent textual annotation above the visualization poses
the question “How accurate have past White House budget forecasts
been?” despite numerous other annotations explicitly describing
inaccuracies in forecasts. _Quotation marks_ and _deliberate_
_understatement_ accomplish similar objectives.
**Similarity** techniques resemble _contrast_ techniques except that
the comparison between two entities is motivated by assumed
similarities between them. One method is _analogy,_ in which a
comparison is made in order to provide insight into the lesser known
of two entities. _Metaphoric statements_ equate two ideas or values by
labelling or directly asserting that one _is_ the other, as in the
visualization titled ‘Speaker Pelosi’s National Energy Tax: A
Bureaucratic Nightmare’ [41]. _Parallelism_ involves expressing two
linguistic statements or visual features to show that they are equal in
importance. An example occurs in ‘How the Recession Changed Us’
(Fig. 1), through the juxtaposition of infographics of roughly the
same size representing different data yet each framed around
negative implications of the recession. _Simile_ resembles analogy and
parallelism but the goal tends to be for effect and emphasis of a
similarity relationship. _Double entendre_ hinges on a linguistic or
visual similarity alone that is used to unite two ideas or entities.
David McCandless’ ‘Poll Dancing’ visualization [29] (Fig. 7, below)
uses both, in the title and vertical visual format.
Finally, **individualization** techniques represent ways to directly
address or appeal to the user as an individual. These techniques are
similar to directly addressing a person using a second-person tense in
language. This can increase interest and ease processing on the part
of the user. _Apostrophe_ is the direct address of the end-user in the
title and annotations attached to a visualization, including rhetorical
questions and suggested goals as mentioned above. More subtle
means of individualization observed in our sample include providing
alternative exploratory functions like _sorting and filtering methods_
(Fig. 6) and _phrasing or imagery framed from an individual-citizen_
_level view_, such as using people icons and phrasing like ‘Buy
Insurance’ that is framed from the ordinary citizen view in the
‘Organizational Chart of the House Democrats’ Health Plan’ [33]
(Fig. 3, top), in which labels like ‘Higher Prices’ that feature
prominently across the top of the graph are framed sympathetic to
the citizen tax-payers’ perspective. Such techniques suggest that the
user adopt a “Cartesian” cultural viewing code that privileges the
individual (section 3.3 below).


3.2.6 Procedural Rhetoric

"Procedural rhetoric" is based in an artifact’s procedural mode of
representation, in other words, the expression of meanings through
rule-based representations and interactive functions [7]. For instance,
Diakopoulos et al. [18] use procedural rhetoric in the form of game
mechanics to drive attention in an interactive information graphic.
The techniques we present here are similar to Segel and Heer’s [38]
suggestions of interactivity features for storytelling in visualizations,
yet are framed from the perspective of the editorial emphases and
omissions they represent. This perspective opens them up for critical
analyses of their rhetorical functions.
**Anchoring** techniques primarily direct a user’s attention in a way
that subsequently helps convey a message. _Default views_ provide an
initial point of interpretation anchored to the default visual
configuration. _Fixed comparisons_ present some information by
default so that users can contrast this information with other values
in the visualization. These can increase engagement via
individualization when values suggested for comparisons are more
likely to be salient to a user. Yet this technique also encourages a
user to look for trends related to a particular data value over other
potential comparisons in the larger data set. The fact that widelyknown methods for judging the ‘visual significance’ of a trend (as



one might judge statistical significance) are lacking among most
users becomes a particular risk. _Spatial ordering_ leverages reading
and scanning conventions to prioritize some information [38].
_Animations_ leverage time to suggest a story, and _partial animation_
that pauses or ends on particular views prioritizes through a
“climactic” effect. More subtle means of anchoring include _search_
_suggestions_ or direct or implied _goal suggestions,_ prompting the user
to examine particular parts of the data rather than explore freely _._
More explicitly interactive techniques include **filtering** _,_ through
search bars or menuing that constrain the data depiction based on a
user’s preferences for certain information (this also appears in
individualization, 3.2.5). Search bars are likely to be effective in
engaging a user to explore data based on how the personalization of
information increases the salience of the message being presented
(e.g. [40]). Menu choices that appear by default can also help users
find the most interesting comparisons or views in a visualization
using the information gained by designers who have already
thoroughly explored the data in the design process.


3.2.7 Patterns of Occurrence

While the output of our coding is indicative of the distribution of
techniques found within our particular sample of narrative
visualizations (i.e. many drawn from journalism outlets), a sample
from other genres of visualization would likely produce a different
distribution. Still, our results allowed comparisons of differences in
the frequency of specific techniques, as well as co-occurrence trends.
The top ten most prevalent techniques (ranked by frequency) were
grouping by color, aggregating values, suggestive spatial mappings,
goal suggestions, bolded fonts, data source citations, metaphoric
statements, color mappings, apostrophe, and variable splices.
A conclusion to be drawn from this ranking concerns the way that
many of these techniques represent common strategies in a wide
variety of data visualizations, based on their perceptual salience (e.g.,
spatial mappings, grouping by color) or their common use in other
facets of communication (e.g., metaphoric statements). The fact that
standard communication strategies can pave the way for potentially
significant rhetorical effects may partially result from our
observation that they often appeared in combination. A designer
might opt to use many less obvious framing strategies to convey a
visualization story, so as to reduce the appearance of bias that can
result from extreme usage of a single strategy.
This ranking excludes several techniques that affected nearly all
visualization, albeit to different degrees. These are variable selection,
default views, knowledge assumptions, and visual contrasts. These
naturally occur very frequently (e.g., an infinite number of variables
cannot be visualized; a starting view for the visualization must be
chosen; some knowledge must be assumed to communicate at all,
such as a rudimentary ability to read charts; the goal of visualization
is to compare data using vision). An insight to be gleaned from even
these, however, arises when one considers that possible alternatives
do exist, but appear to be unconventional. Choosing a default view,
for example, may be unavoidable, but the choice of a single default
view for all users is not a given. Designers might dynamically
choose default views in cases where the goal of the visualization is
less specifically focused on a single intended interpretation. This
particular implementation was not observed however.
Some techniques appeared together quite frequently. Data source
citations tended to appear with other provenance techniques (i.e.,
methodology citations) more often than they appeared alone. While
knowledge assumptions are on some level unavoidable, analogy,
parallelism or other linguistic-based similarity techniques nearly
always occurred with more extreme assumptions. An example is the
title ‘The Arab Powder Keg’, which assumes that the user is familiar
with the powder keg reference. Again, however, we note that this
trend is not inevitable. A designer wishing to create a chart likely to
be understood by the largest number of users could annotate the
presentations with definitions in smaller type so as to include users
without the requisite prior knowledge. Another notable pattern was


HULLMAN AND DIAKOPOULOS: VISUALIZATION RHETORIC: FRAMING EFFECTS IN NARRATIVE VISUALIZATION 2237



the tendency for rhetorical questions to be used with implicit goal
suggestions. In these cases, a question was posed that was most
easily interpreted as ironic or pedantic in light of other annotations
that directly instructed users to look for particular patterns.
A pronounced pattern throughout our analysis was the
observation that the effectiveness of individual strategies depends on
references to other layers of the presentation. This occurs despite the
way that some categories are more closely associated with certain
editorial layers (i.e., linguistic rhetoric mapping to annotations), A
clear example is described below for the ‘Poll Dancing’ visualization
(Fig. 7, Section 4.2), where a double-entendre in the title depends on
several visual metaphors in the graph. This highlights the nature of
narrative visualizations as multimedia artifacts that can’t easily be
reduced to visualization alone.


**3.3** **Viewing Codes**

The concept of **viewing codes** is an adaption of theories presented in
semiotics (e.g., [2]) that capture how attributes of the receiver of an
artifact influence interpretation. Viewing codes are the cultural,
perceptual, cognitive, and psychological lenses that guide how an
end-user (or community) interprets a representation. This concept
sheds light on the constraints imposed on end-user interpretations by
habits and beliefs that are not explicitly contained in the visualization
but rather implied by visualization elements. Below, we discuss how
a distinction between **denotation** and **connotation** becomes

important with regard to discussions of viewing codes.
In semiotic studies, codes are thought of as systems of related
conventions, accumulated over time, that correlate signifiers, or
symbols or representations, with signifieds, or meanings [10]. In
InfoVis, for example, the conventions that dictate what end-users
expect to be communicated by given visualization formats are codes.
Bar graphs, for example, are conventionally associated with discrete
trends, while line graphs are associated with temporal trends. Prior
experience with these graph types informs expectations when faced
with a new graph. When non-temporal data are graphed in a line
graph, users tend to frame their interpretations of the data using
language associated with trends, such as “as a person gets taller they
become more male” [54].
**Cultural codes** describe the social norms and wider beliefs of a
culture that a designer can target to suggest a particular
interpretation. **Individual-level codes** can be higher-cognitive
constraints (e.g., abilities) or more emotionally-based patterns of
reaction. Empirical literature demonstrates how individual
differences deriving from spatial intelligence (e.g., [9]) as well as
prior knowledge can affect visualization interpretation [15, 56] and
even bias perception [19]. For example, individuals differ in their
interests and prior knowledge regarding various types of news.
Consequently, these differences lead to differences in how users
interpret the implications of the story in a narrative visualization.
**Perceptual codes** constrain what is salient to the user given
human visual perception tendencies, such as gestalt principles of
continuation, common fate, and closure [47]. Perceptual tendencies
can combine with internalized knowledge to form additional types of
codes such as **textual codes,** the conventions associated with the
presentation and interpretation of text. With regard to online
information visualizations, these include the common positioning of
the title either in the top center or top left of the presentation, the
inclusion of source and designer credits toward the lower right or left
hand corners of the layout, as well as the assumed left-to-right
reading style in many Western cultures noted by [38]. Similarly,
**aesthetic codes** combine perceptual as well as shared yet subjective
preferences for a particular style of presentation. In the tradition of
visualization design that prioritizes high data-ink ratios, minimalist
techniques such as colorless backgrounds and an avoidance of nonnecessary ornamentation create a particular aesthetic code that can
affect a user’s judgment of the quality of a visualization.
A given element of a visualization-based presentation (whether
textual, visual, or a combination) can activate individual or cultural



viewing codes in several ways. _Denotation_ refers to descriptive
elements, including either textual or visual statements (such as
iconography) that directly attribute features to objects. In the above
example of users’ differing expectations of bar versus line graphs,
the height of the bars directly conveys the value for each bar’s group
for the y-axis variable (e.g., cost, score, or another quantity of
interest). Likewise, the location of the points comprising the line
directly conveys the value of the y-axis in the line graph. Users
familiar with how to read a bar and line graph use this
straightforward mapping to interpret the data. _Connotation,_ however,
refers to cases where a secondary symbol cues, but does not directly
associate, a meaning. This form of communication better describes
why users of a bar graph are more likely to interpret the data as
discrete rather than a temporal trend, while line graphs tend to evoke
temporal interpretations regardless of the data [54]. Users have come
to associate each graph type with particular data types (discrete
categories and temporal trends), and the format itself activates the
code of this expectation despite the lack of explicit reference.


**4** **I** **LLUSTRATING** **V** **ISUALIZATION** **R** **HETORIC**


Two case studies are used to demonstrate the kinds of insights that
the visualization rhetoric framework provides into the interaction of
specific design strategies, their communicative functions, and the
extra-representational factors that constrain them. The first example,
‘Mapping America: Every City, Every Block’ highlights how the
editorial layers described above can be used to convey meaning, and
how specific techniques employed at these levels represent
omissions and emphases of some data over others. The second
example, ‘Poll Dancing’, demonstrates how viewing codes can be
cued through design elements in practice, either through direct
communication (denotation) or implicit suggestion (connotation).


**4.1** **ʻMapping Americaʼ Visualization**

The United States Census represents a nation-wide attempt to
provide an objective view of the demographic distribution of the
country. The New York Times Graphic Department’s ‘Mapping
America: Every City, Every Block’ [6] interactive visualization
depicts 2010 U.S. Census results. Rhetorical techniques are
employed at the four different editorial layers of the visualization
**(** described in section 3.1) to convey the comprehensiveness of the
data collection. At the level of the data, the choice to use actual
census results rather than third-party summaries of the data conveys
the truthfulness of the visualization as a non-biased depiction. The
annotation layer communicates this choice. In this example, social
annotations are provided in the form of comments in the right side
bar that draw attention to important features and suggest conclusions
based on the data. The annotation layer is also leveraged in this
example for **data provenance** purposes, through a _methodology_
_citation_ behind the depiction as well as specific data _source citations_ .
The latter citations may betray _knowledge assumptions_ on the
designers, who wish to appeal to a user’s prior knowledge of the
scope of the census data collection. In the context of visual
journalism, such techniques shape users’ interactions and
interpretations by _signalling transparency_ such that various beliefs
associated with objective information visualizations as a journalistic
standard [23] are cued. Another annotation works as an **uncertainty**
**representation** that conveys impartiality by referencing _the_
_inferential limits_ imposed by a margin of error. The _redundancy_ in
the title annotation phrasing, “Every City, Every Block” [6]
emphasizes the comprehensiveness to the portrayal. Similarly,
techniques using the interactivity layer include a _default zoomed-out_
_view_ of all of New York City (the largest US city and presumed
home of the default New York Times user) and additional zooming
features for gaining an even more holistic view of the country. A
_search bar_ allows users to explore data for any US region using
addresses, zip codes, or city names of personal significance to them.
Together, these choices convey a sense that the visualization
provides a relatively unobstructed presentation of all information


2238 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011


Fig. 7: Partial (left) and full (right) view of David McCandless' 'Poll
Fig. 6: 'Mapping America …ʼ by Bloch et al. of the NYT graphics Dancing: How accurate are poll predictions?' [29].
department [6]. Users can navigate from the initial view in the top
frame to a menu of additional maps using a clickable button.



necessary to decode the patterns inhering in the data. The depicted
story of the spatial distribution of ethnic groups is further supported
by consistent mappings, such as of groups to colors that are applied
identically to data points in the multiple views.
Yet like any visualization, less impartial choices are evident as
well. The choice to represent the families part of the ‘Housing and
Families’ category with a single variable on ‘Same-Sex Couples’
represents an example of information access rhetoric through
**metonomy** _,_ as it omits other families like two parent or single person
households. If additional data was available from the source but the
designers excluded it, this choice can be read as an implicit
suggestion to end-users that they are expected to find this
information more interesting than other family-based variables. The
visual representation carries further emphases on particular views of
data. The choice of which variables are _mapped to salient pre-_
_attentive channels_ [51] leads those variables to be more salient in the
end-user’s interpretation. Here, the use of color leverages the preattentive qualities of this visual encoding channel to represent racial
and ethnic groups, subtly privileging this information.
As described above, interactivity can be used to promote
exploration of specific subsets of the wider range of available
information, subtly privileging some information over other
information. For example, an emphasis is put on the race and
ethnicity information by a default view that **anchors** users’
interpretations so that they are most likely to be formed based on this
dimension of the data. By clicking on a ‘View More Maps’ button in
the example, users are taken to a _menu_ of additional choices, which
enforce the priority of the Race and Ethnicity view by listing this
first, making it more likely that users will interact with these views
as a result of common navigational conventions. Exploring these
additional variables reveals some _ambiguity in variable definitions_ ;
the requirements for membership in the Race and Ethnicity
categories of 'Foreign-born population' and 'Asian population' are not
explained, leaving uncertainty as to what extent these groups
overlap. While ambiguity techniques can function oppositely to
omission techniques by providing a user with the possibility of
several differing interpretations, they also omit more specific
information such that a user is prevented from knowing with
certainty whether her interpretation is supported. Faced with
ambiguity _,_ a user is able to choose for herself which definition or
reading of a visualization element to assume. She may default to the
definition that better supports an interpretation cued by her
individual viewing codes, or unique knowledge and beliefs. This can
work in favor of an intended interpretation on the part of the
designer, such as in cases where providing the full unambiguous
information might eliminate the plausibility of a highly engaging yet
flawed interpretation.



**4.2** **ʻPoll Dancingʼ Visualization**

A second example shows more clearly how extra-representational
constraints can also significantly influence an end-user’s
interpretation. David McCandless’ ‘Poll Dancing: How accurate are
poll predictions?’ [29] (Fig. 7) visualization summarizes the
accuracy of political poll predictions from several years and polling
agencies in a small multiples presentation of vertical line graphs. In
each individual graph of one agency’s predictions over a year,
colored bars representing the political parties are drawn to connect
data points positioned on the y-axis according to the amount of time
prior to the election and on the x-axis according to whether the
predictions fell over (to the right) or under (to the left) of a centered
vertical line representing complete accuracy (or error of zero).
Despite the apparent straightforwardness of the representation,
analysis from a rhetorical standpoint provides insight into several
layers of meaning implied as a result of design choices. Which of
these alternate levels of meaning an individual user prioritizes
depends on the **viewing codes** that constrain the interpretation,
representing a second important insight that can be gained from
rhetorical analysis. In the ‘Poll Dancing’ visualization, the framing
of the poll predictions as ‘dancing’ in the title annotation lines brings
to mind cultural associations with dancing as well as potential
associations that stem from a user’s unique beliefs and knowledge
about dancing. On a more basic level, the word ‘dancing’ combines
with the juxtaposition of the visually-jagged line graphs in a _visual-_
_linguistic metaphor._ Another type of **visual metaphor** is evident in
that the variation, or directionality and distance to the center
‘accuracy’ line of the colored lines in the individual graphs, results in
a _visual noise_ effect. This effect is connected to the dancing
association cued by the title based on a similarity between the
_parallelism_ inherent in the perceptual approximation of movement
achieved by the jagged lines and the movement in dancing. In this
case, the brightly-colored lines also naturally pop out against the
muted grey and white background as a result of a perceptual codes.
An _aesthetic code_ that equates minimalism with representational
impartiality may have motivated the colorless background and low
contrast annotations.
Returning to the central metaphor, based on her prior experience
and associations with political poll predictions, a user might interpret
the association drawn between political poll predictions and the act
of dancing as a light-hearted presentational technique that does not
necessarily comment on the value of political poll predictions. On
the other hand, a user with a more skeptical prior orientation to poll
predictions might interpret the dancing connection as implying a
frivolous or amusing aspect that suggests the results should not be
taken seriously. Hence, differences internalized in _individual codes_
can significantly alter the message an end-user interprets.


HULLMAN AND DIAKOPOULOS: VISUALIZATION RHETORIC: FRAMING EFFECTS IN NARRATIVE VISUALIZATION 2239



Another possible level of meaning can also be inferred given the
specific design elements and consideration of additional associations
that might be created by the title and visual representation. The title
‘Poll Dancing’ implicitly _connotes_ the identically-pronounced term
‘pole dancing’, referring to a form of entertainment and exercise that
traditionally takes place in strip clubs. As such, a second form of
metaphorical substitution, _double-entendre,_ is used to cue a doublemeaning to any users who are aware of the existence and term for
‘pole dancing’ in English. This meaning may gain further support
through another **visual metaphor** cued by the choice to orient the
line graphs vertically and to center the colored lines around the
straight vertical line representing zero error. Users familiar with pole
dancing may associate this vertical line with the pole that a pole
dancer orients her movement around. This _connotation_, if cued in an
end-user with a negative association with ‘pole dancing’ deriving
from cultural stereotypes associated with the activity, might lead to
an interpretation of the visualization’s message as an even stronger
value judgment on the worth of political poll prediction. This results
from the way these negative associations with pole dancing are
metaphorically transferred to political poll predictions.
Interestingly, _connotation_ as that described above depends on
_denotational_ communication of meaning, as the denoted signs are
used in connotation to imply a non-present meaning [2]. In the above
example, the implication of pole dancing achieved by the vertical
representation of the central “pole” relies on the same element that
plays a directly descriptive role by representing the zero point (or
accurate prediction).


**5** **D** **ISCUSSION AND** **F** **UTURE** **W** **ORK**


The study of narrative visualizations offers an opportunity for
increasing understanding of the complementary relationship between
explorative and communicative dimensions in InfoVis. We suggest
several important considerations for this space highlighted by our
analysis, and note areas that may be fruitful for future exploration.
The effects of subtle rhetorical manipulation of information has
generated sometimes surprising results in decision theory and
political and communication studies. Applying a similar
experimental approach to narrative visualizations is a natural
parallel. Our work sets the stage for such studies by providing a
taxonomy of specific information presentation manipulations used in
narrative visualizations. Formal models that have been developed to
capture the formation of user opinions as dependent on personal
attitudes [35] similarly motivate future modelling of combined
effects of rhetorical techniques and personal and cultural viewing
codes on a user’s interpretation in narrative visualization.
Acknowledging the distinction between denotation and
connotation contributes to InfoVis design and theory by highlighting
an epistemological tension that invades many narrative
visualizations. This tension lies between techniques of "objective"
charts informed by transparency ideals on the one hand, and the
layers of connoted interpretation that can seep into or co-opt the
basis of objectivity via rhetorical strategies on the other. The ‘Poll
Dancing’ example leverages the visual representation to precisely
depict trends in forecasting. At the same time, connoted meanings
imply that poll predictions may be best characterized as
“entertaining” rather than rigorous or scientific. The fact that both
modes are possible within the same space may explain why such
visualizations are engaging in ways that is difficult for numeric
representations alone to achieve. The intriguing tension or interplay
that results from combining seemingly oppositional techniques may
help explain how rhetoric can exert a positive influence in
visualizations. Future work includes devising means of assessing
narrative visualizations such that these positive influences are
recognized, while still acknowledging the potential for rhetorical
decisions to negatively affect a user’s accurate interpretation of data.
A frequent example of such a productive tension in our sample is
the tension observable in some narrative visualizations that appear to
be concerned with presenting their work as credible even in cases



where the journalist may have taken some liberties in preparing the
graphic. This is likely the influence of journalistic notions of
transparency, where creators are expected to be upfront about their
knowledge as well as what they don’t know [23]. In many examples,
the journalist’s presence is explicitly stated, such as through notes
about how a visualization contains ‘predictions’ or ‘forecasts’ at the
bottom of the graph (see Fig. 4). These acknowledgements may play
a double role in the sense that they strengthen the sense of the
journalist’s or designer’s integrity despite explicitly pointing to a
lack thereof. This observation dovetails with the observation that
codes or conventions appear to operate in narrative visualizations.
Not only do transparency clues suggest that an end-user should
believe the specific interpretation being emphasized in the
visualization, they also implicitly suggest to users a preferred way of
making similar decisions when viewing other visualizations. Insight
from critical media and semiotic studies suggests that such codes are
dynamic systems that change over time [10]. Many professionally
produced narrative visualizations form part of a larger system of
meaning and rhetoric, knowledge of which guides an informed user
on how to interpret the particular example. By giving more attention
to the development, maintenance, and propagation of such
conventions in information visualization, researchers and designers
alike stand to gain control over dimensions of interpretation that
have remained mostly unaccounted for or underexplored.
A related discussion prompted by this work concerns the degree
of intentionality that can be assumed behind the rhetorical effects
achieved in narrative visualization. In analysis we noted all possible,
although not necessarily intended, framing effects of design choices.
Future studies could involve interviewing visualization creators to
assess their cognizance and intentionality of these methods. In any
case, the power of rhetorical techniques to manipulate user
interpretations supports a call for increased responsibility among
designers to consider the possibly unintended effects their choices
may have. This could, for instance, entail adopting a scenario-based
design approach where different scenarios representing different
viewing codes are considered in an attempt to project how design
decisions could push an interpretation in different directions.
Finally, our analysis concentrated on professionally designed
visualizations, yet it is possible that users contribute to a
visualization story. Examining patterns in user reactions to
visualization rhetoric is a natural next step given the prevalence of
commenting features in online visualization systems (e.g., [49, 50]).
A specific aim for future work concerns the possibility for
integrating rhetorical and communicative features into exploratory
visualization tools, including collaborative visualization systems [11,
42]. Developing a deeper understanding of rhetorical devices and
styles for communicating meaning, particularly those that add
information such as annotations of methodology and uncertainty
representations, could allow analysts to better communicate their
findings to remote or asynchronous others, improving
communication of insights in collaborative visual analytics.


**A** **CKNOWLEDGMENTS**


We wish to thank Eytan Adar, the Michigan Interactive and Social
Computing (MISC) group, and especially the anonymous reviewers
for a wealth of helpful feedback. The second author also
acknowledges support from the NSF and CRA for a Computing
Innovation Fellowship (CIF-197).


**R** **EFERENCES**


[1] P. B. Andersen, What semiotics can and cannot do for HCI, _Knowledge-_
_Based Systems_, vol. 14, 2000.

[2] R. Barthes, _Image-Music-Text_, Hill and Wang, 1978.

[3] S. Bateman, R. L. M, C. Gutwin, A. Genest, D. Mcdine, and C. Brooks,
Useful Junk? The Effects of Visual Embellishment on Comprehension
and Memorability of Charts, _CHI’10_, 2010.

[4] J. Bertin, _Semiology of Graphics: Diagrams, Networks, Maps_, 1st ed.
Univ. of Wisconsin Press, 1984.


2240 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 17, NO. 12, DECEMBER 2011




[5] M. Bloch, A. Cox, J. Craven McGinty and K. Quealy. “A Peek Into
Netflix Queues.” The New York Times, 2010.
http://www.nytimes.com/interactive/2010/01/10/nyregion/20100110netflix-map.html.

[6] M. Bloch, S. Carter, and A. McLean. “Mapping America: Every City,
Every Block.” The New York Times, 2010.
http://projects.nytimes.com/census/2010/explorer.

[7] I. Bogost, Persuasive _Games: The Expressive Power of Videogames_,
The MIT Press, 2007.

[8] S. K. Card, J. Mackinlay, and B. Shneiderman, _Readings in Information_
_Visualization: Using Vision to Think_, 1st ed. Morgan Kaufmann, 1999.

[9] J. B. Carroll, Human cognitive abilities: a survey of factor-analytic
studies, Cambridge University Press, 1993.

[10] D. Chandler, _Semiotics: The Basics_, Routledge, 2001.

[11] N. Chinchor and W.A. Pike, The Science of Analytic Reporting.
_Information Visualization,_ vol. 8, 2009.

[12] D. Chong and J. N. Druckman, Framing Theory, _Ann. Rev. Polit. Sci._
vol. 10, 2007.

[13] W. S. Cleveland and R. McGill, Graphical Perception: Theory,
Experimentation, and Application to the Development of Graphical
Methods, _J. of the Amer. Stat. Assoc._, vol. 79, no. 387, 1984.

[14] W. S. Cleveland, _The Elements of Graphing Data_, 2nd ed. Hobart Press,

1994.

[15] C. Conati and H. Maclaren, Exploring the Role of Individual
Differences in Information, _AVI ’08,_ 2008.

[16] A. Cox. “Budget Forecasts, Compared With Reality”, The New York
Times (online), 2010. Available at
http://www.nytimes.com/interactive/2010/02/02/us/politics/20100201budget-porcupine-graphic.html.

[17] C. S. de Souza, The Semiotic Engineering of Human-Computer
Interaction, The MIT Press, 2005.

[18] N. Diakopoulos, F. Kivran-Swaine, and M. Naaman, Playable Data:
Characterizing the Design Space of Game-y Infographics, _CHI’11,_

2011.

[19] J. Henderson and F. Ferreira, The Interface of Language, Vision, and
Action: Eye Movements and the Visual World, 1st ed. Psych. Press,

2004.

[20] D. Huff, _How to Lie with Statistics,_ W. W. Norton & Company, 1993.

[21] D. Kahneman, P. Slovic, and A. Tversky, _Judgment under Uncertainty:_
_Heuristics and Biases_, 1st ed. Cambridge Univ. Press, 1982.

[22] S. M. Kosslyn, Understanding charts and graphs, _Appl. Cog. Psych._,
vol. 3, no. 3, 1989.

[23] B. Kovach and T. Rosenstiel, The Elements of Journalism: What
Newspeople Should Know and the Public Should Expect, Rev, upd. ed.
Three Rivers Press, 2007.

[24] G. Lakoff, _Women, Fire, and Dangerous Things_, Univ. of Chicago
Press, 1990.

[25] T. Lavin. “How the Recession Changed Us”, The Atlantic, 2010.

Available at

http://www.theatlantic.com/magazine/archive/2011/01/how-therecession-changed-us/8347/

[26] Z. Liu and J. T. Stasko, Mental Models, Visual Reasoning and
Interaction in Information Visualization: A Top-down Perspective,
_IEEE TVCG_, vol. 16, no. 6, 2010.

[27] J. Mackinlay, Automating the Design of Graphical Presentations of
Relational Information, _ACM TOG_, vol. 5, 1986.

[28] R.E. Mayer, M. Hegarty, S. Mayer, and J. Campbell, When Static
Media Promote Active Learning, _J Exp Psych Appl._ vol. 11 no. 4, 2005.

[29] D. McCandless, “Poll Dancing: How Accurate are Poll Predictions?”
Datablog, 2010.
http://www.guardian.co.uk/news/datablog/2010/may/06/generalelection-2010-opinion-polls-information-beautiful#

[30] T. Munzner, A Nested Model for Visualization Design and Validation.
_IEEE TVCG,_ vol. 15, no. 6, 2009.

[31] T. E. Nelson and Z. M. Oxley, Issue Framing Effects on Belief
Importance and Opinion, _J. of Politics_, vol. 61, no. 4, 1999.

[32] D. A. Norman, The Invisible Computer: Why Good Products Can Fail,
the Personal Computer Is So Complex, and Information Appliances Are
the Solution, The MIT Press, 1999.




[33] “Organizational Chart of the Democrats’ Health Plan,” The Website of
the Republican Majority in Congress, 2009.
http://www.gop.gov/resources/library/.../house-democrats-healthplan.pdf

[34] R. Palmer. “Do Not Fuck with Graphic Designers,” Flickr, 2009.
http://www.flickr.com/photos/robertpalmer/3743826461/

[35] W. E. Saris and P. M. Sniderman, Studies in Public Opinion: Attitudes,
Nonattitudes, Measurement Error, and Change, Princeton University
Press, 2004.

[36] N. Schwarz, F. Strack, and H.-P. Mai, Assimilation and Contrast Effects
in Part-Whole Question Sequences: A Conversational Logic Analysis,
_The Public Opinion Quart.,_ vol. 55, no. 1, 1991.

[37] N. Schwarz, H.J. Hippler, B. Deutsch, and F. Strack. Response Scales:
Effects of Category Range on Reported Behavior and Comparative
Judgments, _Public Opinion Quart._, vol. 49, no. 3, 1985.

[38] E. Segel and J. Heer, Narrative Visualization: Telling Stories with Data,
_IEEE TVCG_, vol. 16, 2010.

[39] M. Skeel, B. Lee, G. Smith, and G. Robertson. Revealing Uncertainty
for Information Visualization, _AVI ’08,_ 2008.

[40] C.S. Skinner, V.J. Strecher, and H. Hospers, Physicians’
recommendations for mammography: do tailored messages make a
difference?, _Amer. J. of Public Health_, vol. 84, no. 1, 1994.

[41] “Speaker Pelosi's National Energy Tax: A Bureaucratic Nightmare,”
John Boehner’s office via republicanleader.house.gov, 2009. Original
removed, available at http://voices.washingtonpost.com/ezraklein/2009/06/an_insufficient_respect_for_ch.html.

[42] J. J. Thomas and K. A. Cook. Illuminating the path: The research and
development agenda for visual analytics, IEEE Comp. Soc., 2005.

[43] R. Tourangeau, F.G. Conrad, M.P., Couper, M.P., C. Redline, and C.
Kennedy. The Impact of the Spacing of the Scale Options in a Web
Survey, _Amer. Assoc. for AAPOR ‘08_, 2008.

[44] E. R. Tufte, _Beautiful Evidence_, Graphics Press, 2006.

[45] E. R. Tufte, _The Visual Display of Quantitative Information_, 2nd ed.
Graphics Press, 2001.

[46] A. Tversky and D. Kahneman The Framing of Decisions and the
Psychology of Choice, _Science,_ vol. 211, no. 4481, 1981.

[47] “Vehicle Sales,” _The Economist_, 2010.
http://www.economist.com/blogs/dailychart/2010/12/car_sales.

[48] F. Viegas and M. Wattenberg. Communication-Minded Visualization:
A Call to Action, _IBM Systems Journal,_ vol. 45, no. 4, 2006.

[49] F. Viegas, M. Wattenberg, F. van Ham, J. Kriss, and M. McKeon..
ManyEyes: a Site for Visualization at Internet Scale. _IEEE TVCG,_ vol.
13, no. 6, 2007.

[50] H. Wainer, Picturing the Uncertain World: How to Understand,
Communicate, and Control Uncertainty through Graphical Display.
Princeton University Press, 2009.

[51] C. Ware, _Visual Thinking: for Design_, First Edition. Morgan Kaufmann,

2008.

[52] “When Income Grows, Who Gains?” Economic Policy Institute, 2009.
http://www.stateofworkingamerica.org/pages/interactive#/?start=1999&

end=2008.

[53] W. Willett, J. Heer, J. Hellerstein, and M. Agrawala, CommentSpace:
Structured Support for Collaborative Visual Analysis, _CHI ’11_, 2011.

[54] J. Zacks and B. Tversky, Bars and lines: a study of graphic
communication, _Memory & Cognition_, vol. 27, no. 6, 1999.

[55] C. Ziemkiewicz and R. Kosara, Embedding Information Visualization
Within Visual Representation, _Advances in Information and Intelligent_
_Systems_, vol. 251, Springer Verlag, 2010

[56] C. Ziemkiewicz and R. Kosara, Preconceptions and individual
differences in understanding visual metaphors, _EUROVIS_, 2009.


