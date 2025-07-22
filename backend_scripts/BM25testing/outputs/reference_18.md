IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010

# Narrative Visualization: Telling Stories with Data


Edward Segel and Jeffrey Heer


**Abstract** —Data visualization is regularly promoted for its ability to reveal stories within data, yet these “data stories” differ in important
ways from traditional forms of storytelling. Storytellers, especially online journalists, have increasingly been integrating visualizations
into their narratives, in some cases allowing the visualization to function in place of a written story. In this paper, we systematically
review the design space of this emerging class of visualizations. Drawing on case studies from news media to visualization research,
we identify distinct genres of narrative visualization. We characterize these design differences, together with interactivity and messaging, in terms of the balance between the narrative flow intended by the author (imposed by graphical elements and the interface)
and story discovery on the part of the reader (often through interactive exploration). Our framework suggests design strategies for
narrative visualization, including promising under-explored approaches to journalistic storytelling and educational media.


**Index Terms** —Narrative visualization, storytelling, design methods, case study, journalism, social data analysis.


**1** **I** **NTRODUCTION**



1139



In recent years, many have commented on the storytelling potential
of data visualization. News organizations including the New York
Times, Washington Post, and the Guardian regularly incorporate dynamic graphics into their journalism. Politicians, activists, and television reporters use interactive visualizations as a backdrop for stories
about global health and economics [10] and election results [9]. A recent feature in The Economist [6] explores the proliferation of digital
data and notes that visualization designers are _“melding the skills of_
_computer science, statistics, artistic design and storytelling.”_
Static visualizations have long been used to support storytelling,
usually in the form of diagrams and charts embedded in a larger body
of text. In this format, the text conveys the story, and the image typically provides supporting evidence or related details. An emerging
class of visualizations attempts to combine narratives with interactive
graphics. Storytellers, especially online journalists, are increasingly
integrating complex visualizations into their narratives.
Crafting successful “data stories” requires a diverse set of skills.
Gershon and Page [12] note that effective story-telling _“require[s]_
_skills like those familiar to movie directors, beyond a technical expert’s_
_knowledge of computer engineering and science.”_ While techniques
from oration, prose, comic books, video games, and film production
are applicable to narrative visualization, we should also expect this
emerging medium to possess unique attributes. Data stories differ in
important ways from traditional storytelling. Stories in text and film
typically present a set of events in a tightly controlled progression.
While tours through visualized data similarly can be organized in a
linear sequence, they can also be interactive, inviting verification, new
questions, and alternative explanations.
Currently, most sophisticated visualization tools focus on data exploration and analysis. Applications such as spreadsheets and visualization tools support an array of analysis routines and visual encodings, but beyond exporting images for presentation typically provide
scant support for crafting stories with analysis results. As such, they
provide powerful vehicles for discovering “stories”, but do little to aid
narrative communication of these findings to others. As tools mature
and more richly integrate with the web (e.g., Many Eyes [25], Tableau
Public [22], GeoTime Stories [8]), they are enabling the publication
of dynamic graphics with variably constrained levels of interactivity.
It remains an open question how the design of such tools might be
evolved to support richer and more diverse forms of storytelling.


_• The authors are with Stanford University, Stanford, CA 94305._
_E-mail: {esegel, jheer}@stanford.edu._


_Manuscript received 31 March 2010; accepted 1 August 2010; posted online_
_24 October 2010; mailed on 16 October 2010._
_For information on obtaining reprints of this article, please send_
_email to: tvcg@computer.org._



In this paper, we investigate the design of narrative visualizations
and identify techniques for telling stories with data graphics. We take
an empirical approach, analyzing visualizations from online journalism, blogs, instructional videos, and visualization research. After reviewing related work, we share five selected case studies which highlight varied design strategies and illustrate our analytic approach. We
then formulate a design space constructed from an analysis of 58 examples. Our analysis identifies salient dimensions of visual storytelling, including how graphical techniques and interactivity can enforce various levels of structure and narrative flow. We describe seven
genres of narrative visualization: magazine style, annotated chart, partitioned poster, flow chart, comic strip, slide show, and video. These
genres can be combined with interactivity and messaging to produce
varying balances of author-driven and reader-driven experiences. Finally, we discuss the implications of our framework, noting recurring
design strategies, promising yet under-utilized approaches to integrating visualization with other media, and the potential for improved user
interfaces for crafting data stories. By focusing on the graphical and
interactive elements of narrative visualization, our approach gives less
attention to the cognitive and emotional experience of the reader. We
recognize the importance of these elements, however, and describe directions for future reader-centric research in our conclusion.


**2** **R** **ELATED** **W** **ORK**

Storytelling and visual expression are integral parts of human culture;
storytelling has even been referred to as _“the world’s second-oldest_
_profession”_ [12]. Without summarizing millennia of achievement, we
describe a few of the key concepts informing narrative visualization.


**2.1** **Narrative Structure**

The Oxford English Dictionary defines _narrative_ as “an account of a
series of events, facts, etc., given in order and with the establishing of
connections between them.” Central to this definition is the notion of
a chain of causally related events. Stories of this form often have a
beginning, middle, and end [3, 24]: an introduction to the situation, a
series of events often involving tension or conflict, and a resolution.
Since ancient times, people have tried to understand and formalize
the elements of storytelling. For example, writers (e.g., [5, 19, 21])
have developed typologies of dramatic situations and identified plot
lines common to many narratives, such as the “hero’s journey” [5].
This research typically distinguishes between the content of the story
and the form in which it is told. While stories often concern interacting
characters, they may also present a sequence of facts and observations
linked together by a unifying theme or argument.
Storytelling strategies vary among media and genre. For instance,
stories told through writing have access to a different set of formal
mechanisms and narrative structures (e.g., stream of consciousness)
than stories told through film (e.g., split-screen sequences [3]). Blundell [2] describes narrative devices for journalism such as the _anecdo-_



1077-2626/10/$26.00 © 2010 IEEE    Published by the IEEE Computer Society


1140 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010



_tal lead_ —an initial story, often involving dialogue and characters, that
presents a microcosm of the larger news story—and the _nut graf_ —a
paragraph explicitly describing the news value of an article. These devices are largely unique to journalism, as opposed to literary fiction or
film. Visualizations themselves may incorporate a variety of media,
including text, images and video, and can also be interactive, enabling
stories whose telling relies as much on the reader as on the author.


**2.2** **Visual Narratives**


Artists, designers, and psychologists have all explored ways in which
visual media can be organized to engender a narrative experience.
They have developed nuanced techniques for sequentially directing
a viewer’s attention and keeping viewers oriented across transitions.
While a full treatment of these devices is beyond the scope of this
paper, we present some salient principles here.
Many narratives are rooted in a clear starting point. In visual media,
an establishing shot or overview [3, 19] is often used to introduce the
scene. Of course, not all elements in a scene are of equal importance
throughout a story, and so authors often manipulate a scene to direct
attention to a point of interest. Psychologists have extensively studied phenomena of visual salience [11, 17, 23], showing that outliers
among visual features such as color, size, and orientation preferentially
attract one’s attention. The strength of this attraction is modulated by
multiple factors [17], including the scene itself (e.g., a brightly colored
object is less salient when surrounded by other brightly colored objects) and by the viewer’s task (e.g., expectations and top-down search
can affect what is perceived as most salient).
Cultural factors, particularly reading order (e.g., left-to-right) naturally bias where people look first and how they scan an image [19].
Visual techniques can further establish the order in which the eye
visits elements in the scene. For example, gestalt grouping [26] via
features such as spatial proximity, containment, or connection may
bias one towards first perceiving the grouped content. Vectorial reference [18, 24], most commonly in the form of arrows, is a powerful
technique for sequentially directing attention.
Visual media often involve changes of scene, such as between the
panels of a comic or across cuts in edited film. A number of devices
have been developed to orient a viewer during transitions. Continuity editing techniques in film [3], such as matching on objects or actions, suggest the connection between scenes and may sustain a focus of attention. Similarly, animation design [14, 24] often relies on
object constancy and de-emphasizes secondary details to keep viewers oriented; animators may also subdivide a transition into stages
to facilitate apprehension. Within comics, McCloud [19] proposes a
taxonomy of transition types consisting of _moment-to-moment_ (one
subject, short time period), _action-to-action_ (one subject, longer time
period), _subject-to-subject_ (different subjects, same scene), _scene-to-_
_scene_ (change of scene), _aspect-to-aspect_ (“aspects of a place, idea, or
mood”), and _non-sequitur_ (logically unconnected) transitions. In addition to continuity of objects or actions, extra-pictorial elements [24]
such as callouts (e.g., insets or lines to denote zooming) and annotations are used to enrich a narrative. Not surprisingly, we will see that
many of these techniques are also applicable to narrative visualization.


**2.3** **Storytelling with Data Visualization**


Though data visualization often evokes comparisons to storytelling [6,
7], the relationship between the two is rarely articulated clearly.
Jonathan Harris, the creator of _We Feel Fine_ and _Whale Hunt_, considers himself a storyteller first and a visualization designer second: _“I_
_think people have begun to forget how powerful human stories are, ex-_
_changing their sense of empathy for a fetishistic fascination with data,_
_networks, patterns, and total information... Really, the data is just part_
_of the story. The human stuff is the main stuff, and the data should_
_enrich it.”_ Yet when pressed to describe what he means by “story,”
he responds with only a rough approximation: _“I define ‘story’ quite_
_loosely. To me, a story can be as small as a gesture or as large as a_
_life. But the basic elements of a story can probably be summed up with_
_the well-worn Who / What / Where / When / Why / How.”_



Others have tried to articulate the connection more concretely. Gershon and Page [12] observe that stories communicate information in
a psychologically-efficient format, also a central goal of visualization
design. Using the script of a fictional military scenario as a case study,
they examine tactics used to communicate narrative events, including
continuity editing, highlighting (e.g., flashing), and redundant messaging across media (e.g., audio and video). Still, a deeper understanding
of narrative visualization remains elusive, as _“we need to further un-_
_derstand the characteristic interactions of each genre with each par-_
_ticular audience, its advantages and disadvantages, and how it might_
_affect content and learning.”_ Wojtkowski and Wojtkowski [27] further
argue that what makes data visualization different from other types of
visual storytelling is the complexity of the content that needs to be
communicated. They conclude that _“visual storytelling, in turn, might_
_be of critical importance in providing intuitive and fast exploration_
_of very large data resources,”_ but again stop short of detailing how we
might best _“tailor visualization systems to accommodate storytelling.”_
Some visualization systems have begun to incorporate storytelling
into their design. For example, GeoTime Stories [8] enables analysts
to create annotated stories within visualizations using a text editor and
bookmarking interface. The sense.us [15] system allowed users to create trails of visualization bookmarks that were regularly used for storytelling. Tableau’s graphical histories [13] lets users review, collate,
and export key points of their visual analysis. More recently, Tableau
Public [22] supports the construction and web-based publication of interactive visualizations, supporting storytelling in data-rich domains
such as finance and sports journalism. Such systems provide the first
steps toward making richer storytelling capabilities accessible.
In short, many have observed the storytelling potential of data visualization and drawn parallels to more traditional media. However,
a thorough understanding of the design space for narrative visualization has yet to emerge. In the meantime, practitioners such as artists
and journalists have been forging paths through this space, and we
might hope to gain insight from their explorations. Here we seek to
further our understanding of narrative visualization by analyzing and
contrasting examples of visualizations with a story-telling component.
We then generalize from these examples to identify salient design dimensions. In the process, we hope to clarify how narrative visualization differs from other storytelling forms, and how these differences
introduce both opportunities and pitfalls for its narrative potential.


**3** **C** **ASE** **S** **TUDIES OF** **N** **ARRATIVE** **V** **ISUALIZATION**


We collected visualizations with narrative components, and then attempted to identify and categorize the design features that effectively
tell stories with data. We gathered examples from sources such as online journalism, blogs, visualization books, research papers, and software packages. Our primary source was online journalism, including
visualizations produced by the New York Times, the Guardian, the
Financial Times, the Washington Post, and Slate. Additional visualizations were found through visualization blogs such as Flowing Data,
Infosthetics, and Visual Complexity. For completeness, we also examined visualizations that do not explicitly tell stories but nonetheless
contain relevant storytelling components. We analyzed the narrative
and interactive devices used in each example. The accumulated data
reveals recurring patterns, leading to our analysis in Section 4.
In this section, we present five selected case studies of narrative
visualization. Our goal is to highlight both exemplary and problematic approaches, as well as give the reader a sense of our method of
analysis. Throughout, recurrent design strategies are marked in **bold**
**face** . The examples were chosen to provide a diverse sample of points
in the design space of narrative visualization. These case studies also
highlight the potential application of narrative visualization in fields
ranging across journalism, sports, public policy, and finance.


**3.1** **Steroids or Not, the Pursuit is On**


Baseball star Barry Bonds points to the sky; his goal, 755 home runs,
hovers over his head—“Steroids or Not, the Pursuit is On” [A36].
Shadowing Bonds’ attempt were allegations of steroid use, and many
sports statisticians turned to the numbers to investigate these claims.


SEGAL AND HEER: NARRATIVE VISUALIZATION: TELLING STORIES WITH DATA 1141


Fig. 2. Budget Forecasts, Compared With Reality. New York Times.


**3.2** **Budget Forecasts, Compared With Reality**



Fig. 1. Steroids Or Not, the Pursuit is On. New York Times.


Sized prominently and placed in the upper left corner of the page, the
image of Bonds grabs the eye and points the viewer towards the title,
establishing the topic for the rest of the graphic. A legend consisting of
photos and text introduce Hank Aaron and Babe Ruth, previous home
run leaders whose careers provide points of comparison for Bonds’
career. A line-chart of accumulated home runs shows the three hitters’
careers in alignment, with Bonds’ home runs accelerating at a time
when the other hitters slow down. A shaded **annotation** notes that the
acceleration coincides with the first reports of steroid use in Bonds’
14th season, accompanied by a second annotation just two years later
when Bond takes the lead over Ruth and Aaron. The shaded path then
flows to a similarly-colored inset to the right containing a comparison
of each player’s home run pace after age 34, emphasizing the suspicious acceleration in Bonds’ hitting so late in his career.
The viewer may then move to other sections. On the right, the eye
is invited by a large image of a swinging Alex Rodriguez and a bold
caption noting “Others Taking Aim.” Here we see the other current
players who are chasing the career home run record. The bottom section (“Differing Paths to the Top of the Charts”), devoid of color and
consisting of smaller plots, is given minimum visual priority but completes the story. Small multiples show the home runs per season for
top players on the career home run list, each captioned by a factoid.
The visualization resembles a poster one might see at a science fair,
with the space subdivided into smaller sections, each telling its own
sub-story with charts, pictures, and text. The three sections are linked
together graphically through the use of color, shape, and text. For example, the largest section introduces the hitters according to their order
on the career home run list: Hank Aaron (black line), Babe Ruth (green
line), and Barry Bonds (red line). Subtly **matching on content**, the inset in this section maintains this same scheme, presenting the players
in the same order with their associated colors. This allows the viewer
to immediately discern the reference to the larger image. The section below also begins in the same order (Aaron, Ruth, Bonds) before
proceeding to the other players. This order not only carries informational content (i.e., who has the most home runs) but also prevents the
viewer from having to reorient while switching between sections. Finally, the section to the right charts the performance of current players
over a shadow of the initial chart, a shape we immediately identify as
belonging to Aaron, Ruth, and Bonds.
While these elements provide seamless transitions between sections, they do not dictate the order in which the viewer explores the
visualization. Rather, a path is accomplished through the use of **visual**
**highlighting** (color, size, boldness) and connecting elements such as
arrows and shaded trails. When looking at the visualization, the viewer
begins with the largest image, in part because of its size, central positioning, and coloring, but also because it is capped with a large headline and a picture of Bonds himself telling the viewer where to look.



When deteriorating economic conditions forced a downward revision
in the 2010 White House budget forecast, the New York Times published this visualization [A53] to explore the accuracy of past budgets’
predictions. A large headline is followed by a brief prompt introducing the visualization. Below are two panels side by side. The left
panel contains another bold headline accompanied by a short paragraph of text, while the right panel contains a line chart showing budget surpluses and deficits between 1980-2020, with the estimates distinguished from actual data using annotations and coloring. Just above
these panels is a **progress bar** indicating the length of the visualization
and providing the user with a mechanism to navigate between slides.
As the user steps through the presentation, the visualization maintains a **consistent visual platform**, changing only the content within
each panel while leaving the general layout of the visual elements intact. Each new slide alters the text in the left panel, while updating the
chart in the right panel with animated transitions. A narrative is communicated clearly through the interaction of the text in the left panel
with the annotations and graphic elements in the right panel, each enriching the narrative through **multi-messaging**, providing related but
different information [20]. In this way, the presentation guides the
viewer through historical budget forecasts, explaining patterns in the
data ( _80% of deficit forecasts have been too optimistic_ ) and highlighting key events ( _surpluses under Clinton were generated in part by_
_a stock market bubble_ ). Users can discover additional statistics by
mousing-over the chart, revealing **details-on-demand** with the years
and estimates of past forecasts. Halfway through the presentation, a
**timeline slider** appears above the dates on the horizontal axis, with the
slider position updating along with the chart above. Text on the fifth
slide explicitly encourages the user to interact with this slider to isolate forecasts for a single year. The presentation ends with the current
budget forecasts for 2012, letting the user see how these predictions
change under different economic assumptions.
At its core, this visualization is a typical slide-show presentation
augmented by two important features. First, it allows the user to determine the pace of the presentation by using the provided progress
bar. And second, it allows the user to interact with the presentation by
mousing-over areas of interest and by using the slider to explore different time windows. We call this structure an **interactive slideshow**
that uses **single-frame interactivity**, meaning that interaction manipulates items within a single-frame without taking the user to new visual
scenes. These devices encourage the user to explore the data within the
structure of an overarching narrative. The narrative functions in two
ways, both communicating key observations from the data, as well
as cleverly providing a **tacit tutorial** of the available interactions by
animating each component along with the presentation. By the time
the presentation encourages the user to investigate budget forecasts for
specific years, it is already clear to the user how to do this.
This presentation style can be compared to a narrative pattern called
the **martini glass structure** [4], following a tight narrative path early
on (the stem of the glass) and then opening up later for free exploration (the body of the glass). Different features of the visualization


1142 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010



Fig. 3. Afghanistan: Behind the Front Line. Financial Times.


ensure that the viewer does not lose his place in the narrative during
this exploratory stage, with orientation provided by the consistency of
the visual platform, the updating progress bar, and the timeline slider.


**3.3** **Afghanistan: Behind the Front Line**


In an effort to draw popular support away from the Taliban, NATO
deployed groups of soldiers and civilians known as Provincial Reconstruction Teams (PRTs) to Afghanistan to implement nation-building
development projects. People began to question the effectiveness of
these groups amidst escalating violence in the region. This visualization [A45] begins with a traditional newspaper headline and brief
article introducing the PRT’s mission. The article then states the intended purpose of the graphic: to establish indicators of success by
which to evaluate the development work being done in Afghanistan.
The graphic starts with its own introduction as well, occupying
the first of four tabs the user can select. This starting tab contains
only introductory text and a photograph of a US soldier. The remaining tabs (Nation-building, Security, Counter-narcotics) each contain
an identical map of Afghanistan subdivided by province. A different
hue (green, blue, red) is used to color the map for each tab, providing a **semantically consistent** color encoding; brightness encodes the
values for each province. To the upper left of the map is a legend
which changes according to the tab’s content. The “Nation-Building”
tab tracks the overall cost of activities for each province, “Security” tracks the severity of insurgent activity, and “Counter-Narcotics”
tracks opium cultivation. This last tab also contains a **timeline slider**,
allowing the user to explore how opium cultivation has changed over
the past five years of the PRT’s efforts.
Each tab contains an interactive list of NATO countries on the right.
A short message and mouse pointer indicate the list is interactive.
Clicking an individual country highlights the provinces in which that
country has troops deployed, outlining their borders with a flashing
red line. A paragraph of text appears in a panel below, providing
facts about that country’s involvement, and in some cases allowing the
user to isolate particular activities (Education, Health, Economic Development, etc.). Finally, a button labeled “PRT INFO” slides down
a new window containing additional background about the PRTs in
Afghanistan, with **details-on-demand** for each country involved.
The visualization maintains the same graphical layout across tabs,
modified only slightly for the different content. This **consistent visual**
**platform** provides easy transitions between tabs, and the colors serve
as an indication that a switch has occurred. The visual highlighting
of provinces serves to draw the viewer’s eye to the relevant areas, a
necessary feature given the density of the map. Finally, each interactive component is clearly adorned with **markers of interactivity**,
explicitly pointing out the potential for interaction.
However, we believe that some aspects of the visualization could be
improved. Most importantly, the overall structure does not sufficiently



Fig. 4. Human Development Trends. Gapminder.


guide the viewer through the data, making it hard to draw meaningful conclusions from the large amount of information available. Why
do some regions cost more than others? (Annotations are needed on
the map.) Which countries provide the best aid? (Comparisons are
needed between countries.) What projects exist in a particular region?
(Regions cannot be selected.) Moreover, too much information is provided for each country in terminology-heavy paragraphs that are difficult to parse. While this may be useful for a trained analyst, a general
audience would be better served by replacing the vast quantity of information with memorable factoids. The graphic may suffer by putting
exploratory power into the hands of the viewer without sufficient guidance. A **synthesis or summary** could be very useful toward this end.


**3.4** **Gapminder Human Development Trends**


This **interactive slideshow** [A47] surveys trends in global income and
health. The visualization begins with a grid of screenshots from different sections of the presentation (Figure 4), with each image labeled
with its respective topic (Income, Poverty, Health, Deaths, etc.). This
**checklist structure** [20] provides an establishing shot of the content
to be covered and serves as a reminder of what each section contains
once the presentation is finished. It also enables navigation to particular segments. A **progress bar** at the bottom of the screen mirrors
the grid above, while a large “Start” button in the lower right corner,
highlighted by an animated pointer, tells the viewer how to begin the
presentation. This button turns into familiar browser-style “forward”
and “back” buttons when clicked, letting the user navigate between
slides at his own pace. A second progress bar also appears upon entering each individual section. Both progress bars also serve as navigation tools, allowing the user to skip around the presentation without
relying on the stepwise navigation provided by the browser buttons.
The presentation contains three basic kinds of charts: histograms,
scatter plots, and bar charts. However, no individual section utilizes
more than one chart type. Importantly, changes between chart types
are made explicit in order to avoid confusing the viewer. For example, when the presentation transitions from histograms to scatterplots
between Sections 3 and 4, a staged **animated transition** morphs the
chart types across several patient steps (see Figure 5). Even manipulations within a single chart receive this same attention: in Section 3, a
comment _“Zooming in below the poverty line”_ alerts the viewer to the
upcoming manipulation before it occurs.


Fig. 5. Staged animated transitions between chart types.


SEGAL AND HEER: NARRATIVE VISUALIZATION: TELLING STORIES WITH DATA 1143



Each section walks the user through a visualized dataset, pointing out key observations along the way. These explanations rely on
a combination of **annotations**, **highlighting**, **animated transitions**,
and **single-frame interactivity** . Typically, the data is not presented
all at once. Rather, each chart is constructed in a stepwise fashion,
with annotations and animations explaining each stage of the process.
In Section 1, the x-axis initially appears without the rest of the chart,
introduced with the comment, _“Daily income is measured in dollars_
_per day.”_ In Section 2, the graphic incorporates the data for each geographic region individually, reserving the pauses between animations
to offer facts about the region ( _Africa: Population 630 million_ ). At
any point in these lessons, the user can mouse over different graphical
elements for **details-on-demand** .

Beyond simply introducing graphical features, the annotations convey a narrative for each section, providing observations that the viewer
would unlikely identify on his own. For example, Section 3 explains
_“In the 1970s most poor lived in South and East Asia.”_ Then, as the
timeline moves forward and the chart changes, a new comment states,
_“The last 30 years changed the face of global poverty. Now Africa is_
_the home of one third of all poor.”_ A final animation updates the chart
even further, this time with the comment, _“In 2015 Africa will account_
_for the majority of the world poverty.”_ These narratives crucially allow dense information to be quickly comprehended by the user, and
the graphical elements play an important role in making this possible:
animations highlight relevant sections of the charts, color schemes remain **semantically consistent** between slides, and arrows and labels
regularly appear to clarify elements mentioned in text.
Periodically the presentation allows increased user interactivity
with the display, typically after a narrative segment is complete, again
following a **martini glass structure** . In this presentation, the increased interactivity occurs most frequently in segments using timeseries data, as a **timeline slider** appears to let the user return to previous years. Importantly, the exposed interactivity is part of the narrative, not merely an afterthought. For instance, Section 3 explains _“The_
_global goal of halving poverty by 2015 will be met because of fast_
_progress in Asia. But on current trends Africa and Latin America will_
_not meet that goal.”_ At this point, additional interactive components
appear on the display and a prompt appears with the message _“Use_
_the timebar to see people in Asia moving out of poverty.”_ In this way,
the interactivity is actually a continuation of the story, emphasizing
the same themes and encouraging the user to use the story as a starting
point for his own personal exploration of the data.


**3.5** **The Minnesota Employment Explorer**


Months before the stock market crash of September 2008, many observers noted that the economy was slowing down; unemployment was
rising while gas and food prices neared record highs. In January 2008,
Minnesota’s state economist had seen enough to say the state was in
recession. In response, in July 2008 Minnesota Public Radio (MPR)
released a feature on their website on the “Minnesota Slowdown.” The
page links to stories detailing the state’s economic malaise and shares
interviews with residents hit hard by the downturn.
At the bottom of the page lies an interactive visualization of state
unemployment data: The Minnesota Employment Explorer [A19], a
joint effort of MPR and the UC Berkeley Visualization Lab. Small
multiples of time-series charts show normalized unemployment data
by industry from 2000 to 2007. Both long-term trends and seasonal oscillations are apparent. For example, the Health sector exhibits steady
growth, while agriculture, construction, and education show strong
seasonal patterns. Mouse-hover provides **details-on-demand** ; doubleclicking an industry triggers a drill-down into that sector, with an **ani-**
**mated transition** updating the display to show sub-industry trends.
Notably, the visualization also includes social interaction features.
A list of comments associated with the current view enables journalists
and readers to share observations and discuss trends. Commentary
and visualization are linked together: one can select a data series to
highlight it in the view; the highlight is subsequently saved with the
comment. Selecting a comment reveals these annotations. Conversely,
selecting a series highlights related commentary.



Fig. 6. Minnesota Employment Explorer. Minnesota Public Radio.


The goal of the visualization was to engage readers in finding and
telling their own stories in the data. It was hoped that residents in various occupations would engage in social data analysis [15], sharing
expertise from their respective industries. Despite good intentions, the
visualization largely failed in this goal. A total of 23 people submitted
62 comments, with 25 of these comments being posted by the producers of the visualization. Other guests pointed out trends of interest
and shared pointers to other related data sets; for example, a registered
nurse shared his first-hand experiences in the Health sector. However,
the majority of posters were not citizens of Minnesota; they were visualization and statistics enthusiasts drawn by the technology (the piece
was mentioned on a popular visualization blog) and not by the story.
A post-mortem analysis reveals multiple areas for improvement.
Some issues revolve around usability: the visualization was placed
below-the-fold on the web site, and thus possibly overlooked by MPR
readers. The visualization also lacked a **tacit tutorial** —it dropped
readers into the data with little orientation and no example of a rich,
emergent story. Seed comments served to highlight interesting patterns and raise questions, but did not develop a larger narrative.
Most importantly, the graphics are disconnected from the narrative.
While unemployment statistics are topically relevant to the feature,
they were not related to any of the other news stories. Moreover, only
unemployment data from 2000-2007 was available from the state at
that time—yet the main concern of the feature is the economic woes of
2008. Though the Employment Explorer was designed with the hopes
of having people _annotate data with stories_, this example suggests
that it may be more fruitful to first _annotate stories with data_ . By
immersing readers in a narrative and providing a tacit tutorial, readers
may become invested in exploring new perspectives of a story—and
perhaps branch out in search of new stories of their own.


**4** **D** **ESIGN** **S** **PACE** **A** **NALYSIS**


We seeded our choice of design space dimensions using related work
in film, comics, and art. In particular, McCloud’s “Making Comics”

[20] provides a robust taxonomy of visual elements that contribute to
storytelling. Our ideas evolved as we analyzed more examples and
observed emerging patterns. These observations allowed us to further organize the design features into increasingly coherent categories,
such as genre types for narrative visualizations and different methods
of integrating visualizations with accompanying text. Our final categories depict unique patterns for narrative visualization, distinguishing
itself from other forms visual storytelling. For example, interactive visualizations allow users to manipulate the display, introducing design
decisions that do not apply to non-interactive media.
We represent the design space in a table that relates each example
to specific design strategies observed across the dataset. In total we
analyzed 58 visualizations using the case study method illustrated in
Section 3. The examples were taken from online journalism (71%),
business (20%), and visualization research (9%). We optimized our


1144 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010


|Architecture and Justice (Brooklyn Crime Blocks) Columbia Univ. SIDL John Snow’s Chart of Deaths from Cholera Edward Tufte Politicians Abuse their Free-mailing Privileges before Elect Edward Tufte Football Drawings Visual Complexity Pedestrians Crossing the Street Visual Complexity The Climate Agenda Washington Post When Did Your County's Jobs Disappear? Washington Post Acadametrics House Price Index Financial Times Banks’ Earnings: How Compensation Relates to Performa Financial Times Deadly Offensive: Taliban Attacks in Pakistan Financial Times GDP Moves by Sector Financial Times UK Economic Data Financial Times Budget 2010: Reaction from around the UK Guardian Formula One 2010: Driver's Rankings Guardian Lighting Up Hadrian's Wall Guardian Mapping Hydropower Hotspots across the UK Guardian Moscow Metro Bombs: interactive map Guardian The World Economy Turns the Corner Guardian Minnesota Employment Explorer Minnesota Public Radio A Map of Olympic Medals New York Times All of Inflation's Little Parts New York Times Paths to the Top of the Home Run Charts New York Times The Ebb and Flow of Movies: Box Office Receipts 1986 — New York Times The Jobless Rate for People Like You New York Times Advertisement: Bus United Technology Advertisement: Helicopter United Technology Analyzing Obama's Schedule Washington Post Oscars 2010: The Best Picture Nominees Guardian The Consumer and Retail Price Indices since 2006 Guardian UK Voting Intentions Guardian Comparison of Bear Markets New York Times Faces of the Dead New York Times How Americans Spend Their Day New York Times Michelle Obama's Family Tree New York Times NetFlix Rentals New York Times Steroids or Not, the Pursuit is On New York Times Vancouver's Olympic Venue New York Times On the Map: Five Major North Korean Prison Camps Washington Post Spheres of Influence: The Bush Campaign Pioneers Washington Post A Visual Guide to the Financial Crisis Flowing Data Economic Meltdown of 2008-2009 Flowing Data Where Did All the Money Go? Flowing Data Life Cycle of a Beetle through a Year Edward Tufte McCloud's Making Comics Scott McCloud Afghanistan: Behind the Front Line Financial Times Toyota Timeline: A Company History Financial Times Gapminder Human Development Gapminder Earthquakes: Why They Happen Guardian Iran's Nuclear Programme Guardian Shaun White's Double McTwist Guardian Toyota's Stick Accelerator Problem Guardian Alpine Skiing, From Technical Turns to Tucks and Speed New York Times Budget Forecasts vs. Reality New York Times How the Government Dealt with Past Recessions New York Times Mac Orientation Video Apple Delta Airplane Safety Video Delta The Story of Stuff Story of Stuff Project Virgin America Airplane Safety Video Virgin America|Visualization Description Source|Col3|
|---|---|---|
|+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+|Magazine Style<br>Annotated Graph / Map<br>Partitioned Poster<br>Flow Chart<br>Comic Strip<br>Slide Show<br>Film / Video / Animation|**Genre**|
||||
|�<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>�<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>-|Establishing Shot / Splash Screen<br>Consistent Visual Platform<br>Progress Bar / Timebar<br>"Checklist" Progresss Tracker<br>**Visual Structuring**|**Visual Narrative**|
|+<br>+<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>+<br>-<br>�<br>�<br>�<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>�<br>�<br>�<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>-<br>-<br>-<br>�<br>�<br>�<br>+<br>+<br>+<br>�<br>�<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+|Close-Ups<br>Feature Distinction<br>Character Direction<br>Motion<br>Audio<br>Zooming<br>**Highlighting**|Close-Ups<br>Feature Distinction<br>Character Direction<br>Motion<br>Audio<br>Zooming<br>**Highlighting**|
|�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>�<br>�<br>�<br>�<br>�<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>�<br>�<br>�<br>+<br>�<br>+<br>+<br>�<br>�<br>+<br>�<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+|Familiar Objects (but still cuts)<br>Viewing Angle<br>Viewer (Camera) Motion<br>Continuity Editing<br>Object Continuity<br>Animated Transitions<br>**Transition Guidance**|Familiar Objects (but still cuts)<br>Viewing Angle<br>Viewer (Camera) Motion<br>Continuity Editing<br>Object Continuity<br>Animated Transitions<br>**Transition Guidance**|
||||
|-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>+<br>**1**|Random Access<br>User Directed Path<br>Linear<br>**Ordering**|**Narrative Structure**|
|�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>-<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>-<br>+<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>�<br>**2**<br>**3**|Hover Highlighting / Details<br>Filtering / Selection / Search<br>Navigation Buttons<br>Very Limited Interactivity<br>Explicit Instruction<br>Tacit Tutorial<br>Stimulating Default Views<br>**Interactivity**|Hover Highlighting / Details<br>Filtering / Selection / Search<br>Navigation Buttons<br>Very Limited Interactivity<br>Explicit Instruction<br>Tacit Tutorial<br>Stimulating Default Views<br>**Interactivity**|
|+<br>-<br>+<br>-<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>�<br>-<br>+<br>+<br>-<br>-<br>+<br>�<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>-<br>-<br>-<br>-<br>-<br>-<br>�<br>+<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>-<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>+<br>-<br>+<br>+<br>+<br>-<br>-<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>-<br>+<br>-<br>+<br>-<br>+<br>-<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>-<br>+<br>+<br>+<br>+<br>+<br>-<br>-<br>-<br>-<br>-<br>+<br>-<br>-<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>+<br>+<br>+<br>�<br>+<br>+<br>�<br>+<br>-<br>-<br>-<br>+<br>+<br>-<br>-<br>**4**|Captions / Headlines<br>Annotations<br>Accompanying Article<br>Multi-Messaging<br>Comment Repitition<br>Introductory Text<br>Summary / Synthesis<br>**Messaging**|Captions / Headlines<br>Annotations<br>Accompanying Article<br>Multi-Messaging<br>Comment Repitition<br>Introductory Text<br>Summary / Synthesis<br>**Messaging**|


SEGAL AND HEER: NARRATIVE VISUALIZATION: TELLING STORIES WITH DATA 1145



collection to include visualizations that contained clear sequences of
narrative events, a diversity of visualization genres (e.g., flow charts,
slide shows), and a range of interaction strategies (e.g., filtering, timelines). Using these criteria, we sampled from our initial larger pool of
examples to arrive at the resulting 58 items featured in Fig. 7. However, we do not claim that our sample is exhaustive, as we did not
canvas other potential sources such as video games or e-learning tools.
The table uses dark blue and a plus-sign (+) to indicate the presence of a particular feature; light blue and a minus-sign (-) indicate
that an example does not use that feature. In some cases a cell is colored grey to indicate that a design feature is precluded by the medium
rather rather than omitted by explicit design choices. For instance, we
did not analyze visualizations on printed paper with respect to interaction or animation. That said, some workarounds to medium limitations are possible: comics can use a multi-panel series of increasing
close-ups to convey the same effect as camera zoom [20], and static
visualizations might employ a choose-your-own-adventure format to
allow viewers to determine their own path through the content.
We arrived at our categories after much iterative organization (e.g.,
affinity diagramming [1]) of individual design features. We attempted
to be consistent in our evaluation of each example. As our categories
evolved, we reconsidered previous examples, re-categorizing as appropriate. We acknowledge there is some inevitable subjectivity when
imposing a taxonomy over a diverse set of designs.


**4.1** **Design Space Dimensions**


Our organization of the design space contains three divisions of features: (1) genre, (2) visual narrative tactics, and (3) narrative structure
tactics. The first division identifies the _genre_ of each visualization, a
taxonomy of visual narrative types described later in section 4.3.
The second division identifies _visual narrative_ tactics: visual devices that assist and facilitate the narrative. This division is subdivided into three sections: (i) visual structuring, (ii) highlighting, and
(iii) transition guidance. _Visual structuring_ refers to mechanisms that
communicate the overall structure of the narrative to the viewer and
allow him to identify his position within the larger organization of the
visualization. These design strategies help orient the viewer early on
(establishing shot, checklist, consistent visual platform) and allow the
viewer to track his progress through the visualization (progress bar,
timeline slider). _Highlighting_ refers to visual mechanisms that help
direct the viewer’s attention to particular elements in the display. This
can be achieved through the use of color, motion, framing, size, audio, and more, which augment the salience of an element relative to its
surroundings. Many of these strategies are also used in film, art, and
comics. _Transition guidance_ concerns techniques for moving within
or between visual scenes without disorienting the viewer. A common
technique from film is continuity editing, though other strategies (e.g.,
animated transitions, object continuity, camera motion) also exist.
The third division identifies _narrative structure_ tactics used by each
visualization, or non-visual mechanisms that assist and facilitate the
narrative. This division is further divided into three sections: (i) ordering, (ii) interactivity, and (iii) messaging. _Ordering_ refers to the ways
of arranging the path viewers take through the visualization. Sometimes this path is prescribed by the author (linear), sometimes there is
no path suggested at all (random access), and other times the user must
select a path among multiple alternatives (user-directed). _Interactivity_
refers to the different ways a user can manipulate the visualization (filtering, selecting, searching, navigating), and also how the user learns
those methods (explicit instruction, tacit tutorial, initial configuration).
Finally, _messaging_ refers to the ways a visualization communicates
observations and commentary to the viewer. This might be achieved
through short text fields (labels, captions, headlines, annotations) or
more substantial descriptions (articles, introductions, summaries).


**4.2** **Design Space Observations**


Three important patterns stand out from the data: (1) the clustering of
different ordering structures, (2) the consistency of interaction design,
and (3) the under-utilization of narrative messaging.



Fig. 8. Genres of Narrative Visualization.


The first pattern can be observed by the clusters of dark blue in
the ordering section, suggesting clear differences between how visualizations guide the viewer through their content (Figure 7(1)). These
clusters correspond to narrative formats such as slide shows, comic
strips, annotated graphs, and others. We use these ordering types to
identify distinct genres of visual narratives in Section 4.3.
The second pattern highlights the consistency in interaction design
choices made by visualizations. Across the examples, we see the same
interactive techniques being used (Figure 7(2)): hover highlighting
and details-on-demand, limited interactivity, explicit instruction for
interactive functionality, and navigation buttons when the visualization contains more than one frame (e.g., slideshows). The table also
shows the consistent under-utilization of “tacit tutorials” and “stimulating default views” (Figure 7(3)). Tacit tutorials introduce a visualization’s interactive functionality by animating the interactive components along with the presentation to make it clear how to manipulate
the display. As a result, the user becomes familiar with the interactive capabilities of the visualization without requiring explicit instructions. Stimulating default views provide initial presentations of data
and analysis intended to excite the user, a device analogous to journalistic leads. These views can then be used as jumping off points for
further exploration. Both these techniques can be seamlessly incorporated into the visualization’s design while simultaneously engaging
the user in the interactive functionality.
The third pattern shows the under-utilization of common narrative
messaging techniques such as repetition of key points, introductory
texts, and final summaries and syntheses (Figure 7(4)). In particular, the data shows that interactive graphs do not include sufficient
commentary for narrative purposes, with little use of repetition, multimessaging (i.e., text, images, and audio working together), or annotations to emphasize key observations from the data. Note that narrative messaging techniques are more frequently used in Slideshows
and Videos, as these genres put more effort into communicating the
narrative intended by the author. This may explain why qualitatively
these visualizations feel more like “stories” and less like data tools.


**4.3** **Genres of Narrative Visualization**

We found that our examples can be characterized by the 7 basic _genres_
shown in Figure 8: magazine style, annotated chart, partitioned poster,
flow chart, comic strip, slide show, and film/video/animation. These
genres vary primarily in terms of (a) the number of frames—distinct
visual scenes, multiplexed in time and/or space—that each contains,
and (b) the ordering of their visual elements. For example, an image
embedded in a page of text (“magazine style”) has only a single frame,
while a comic may have many frames. A multi-view visualization
(“partitioned poster”) may suggest only a loose order to its images,
while a comic strip tends to follow a strict linear path.
These genres are not mutually exclusive: they can function like
building blocks, combining to produce more complex visual genres.
The Barry Bonds visualization ( _§_ 3.1) is part Partitioned Poster and
part Flow Chart, presenting multiple images simultaneously while using Flow Chart tactics to suggest a path to the viewer. Both the Budget Forecast ( _§_ 3.2) and the Gapminder ( _§_ 3.4) examples use Annotated
Graphs but within a Slide Show format.
Though each of these genres can be used to tell a story, we note
that different genres work better for different story types. Choosing
the appropriate genre depends on a variety of factors, including the


1146 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010



Table 1. Properties of Author-Driven and Reader-Driven Stories. Most
visualizations lie along a spectrum between these two extremes.


**Author-Driven** **Reader-Driven**

Linear ordering of scenes No prescribed ordering
Heavy messaging No messaging
No interactivity Free interactivity


complexity of the data, the complexity of the story, the intended audience, and the intended medium. There are clear cases in which a
genre is more appropriate for a particular purpose. Business presentations typically use Slide Shows instead of Comic Strips, and television
commercials use Videos instead of Flow Charts. These are common
and intuitive cases, but not all instances are so clear cut. For example,
it is not obvious whether students might learn best from a Slide Show
or a Video or even a Comic Strip. The right choice also depends on
the content being presented and the students’ background. In general,
there will be no “right answer” _a priori_, but several possible candidates, each with advantages and disadvantages.
Both messaging and interactivity can be layered on top of these genres. Messaging is the use of text to provide observations and explanations about the images. Typically this text takes familiar forms such as
headlines, captions, labels, and annotations. For some visualizations,
messaging can also include audio. Note that messaging is optional for
any of the genres above, and can vary widely between instances of the
same genre. Interactivity allows the visualization to be manipulated
by the viewer. There are many possible types and degrees of interactivity, though common forms in narrative visualization include navigation buttons, hover highlighting, hover details-on-demand, filtering,
searching, drill-down, zooming, and time sliders. Importantly, the appropriate use of messaging and interactivity will depend on a variety
of factors. Messaging might clarify visual elements but produce clutter. Interactivity might engage the user but detract from the author’s
intended message. Again, these tradeoffs require context-specific consideration and judgment.


**4.4** **Balancing Author-Driven and Reader-Driven Stories**


The visual narrative genres, together with interaction and messaging,
must balance a narrative intended by the author with story discovery
on the part of the reader. We thus place narrative visualizations along a
spectrum of **author-driven** and **reader-driven** approaches (Table 1).
A purely author-driven approach has a strict linear path through the
visualization, relies heavily on messaging, and includes no interactivity. Examples include film and non-interactive slideshows. A strongly
author-driven approach works best when the goal is storytelling or
efficient communication. We see this approach used in comics, art,
cinema, commercials, business presentations, educational videos, and
training materials.
A purely reader-driven approach has no prescribed ordering of images, no messaging, and a high degree of interactivity. Examples include visual analysis tools like Tableau or Spotfire. A reader-driven
approach supports tasks such as data diagnostics, pattern discovery,
and hypothesis formation.
Historically, many visualizations fall into the author-driven or
reader-driven dichotomy. However, as we have seen throughout our
case studies, most examples of narrative visualization fall somewhere
in-between, and an important attribute of narrative visualization is its
flexibility in balancing both elements. Visualizations are increasingly
striking a balance between the two approaches, providing room for
limited interactivity within the context of a more structured narrative.
This is a relatively recent development, with most mainstream examples coming from online journalism.
All the interactive examples in our dataset use a mix of the authordriven and reader-driven approaches. Despite the range of possible
combinations, a few hybrid models have become most common. Below we discuss three common schemas. The first structure prioritizes
the author-driven approach, the second structure promotes a dialogue
between the two approaches, while the third structure prioritizes the
reader-driven approach.



4.4.1 Martini Glass Structure


The Martini Glass visualization structure begins with an author-driven approach, initially
using questions, observations, or written articles to introduce the visualization. Occasionally no text is used at all, as the visualization
instead relies on an interesting default view or annotations. Once the
author’s intended narrative is complete, the visualization opens up to
a reader-driven stage where the user is free to interactively explore the
data. The structure resembles a martini glass, with the stem representing the single-path author-driven narrative and the widening mouth
of the glass representing the available paths made possible through
reader-driven interactivity. Using this image, we can think of varying
degrees of authoring (question, observation, article) as corresponding
to different stem types (short, long), and varying degrees of readership (highlighting, filtering, path-choosing) corresponding to different
mouth shapes. With all these permutations, the general structure remains intact, with the author-driven narrative functioning first, then
followed separately by the reader-driven interactions. The authoring
segment may function as a jumping off point for the reader’s interaction, with questions, observations, and themes suggesting the types of
issues a reader might explore on his own. This structure is the most
common across the interactive visualizations we examined.


4.4.2 Interactive Slideshow


The Interactive Slideshow structure follows a
typical slideshow format, but incorporates interaction mid-narrative within the confines of each slide. This structure
allows the user to further explore particular points of the presentation
before moving ahead to the next stage of the story. We saw this structure in both the Budget Forecasts ( _§_ 3.2) and Gapminder ( _§_ 3.4) case
studies. Contrary to the martini glass, an interactive slideshow allows
for interaction mid-narrative, a more balanced mix of author-driven
and reader-driven approaches. However, individual slides often function in the martini glass style, again communicating author-intended
messages prior to prompting the user to interact with the display.
Interactive slideshows work well with both complex datasets and
narratives. For complex datasets, this structure allows the author to
walk the user through data-dimensions and manipulations step-bystep. This ensures that the user only moves forward in the presentation
when he is ready to do so, and allows the user to repeat steps if desired.
For complex narratives, this format allows the author to draw discrete
boundaries between different story segments, similar to a cut in film.


4.4.3 Drill-Down Story


The Drill-Down Story visualization structure
presents a general theme and then allows the
user to choose among particular instances of that theme to reveal additional details and backstories. For instance, the theme might be “Historical Bear Markets” [A31] and the visualization will allow the user
to drill-down to a particular bear market to learn more about its history. Or a map showing “North Korean Prison Camps” [A38] may
allow the user to learn more about individual camps by clicking on a
specific location on the map. This structure puts more emphasis on the
reader-driven approach, letting the user dictate what stories are told
and when. Nevertheless, it still requires significant amounts of authoring to determine the possible types of user interaction, what candidate
stories to include, and the details included for each story.


**5** **D** **ISCUSSION**


In this paper, we conducted a design space analysis of narrative
visualization—visualizations intended to convey stories—based on a
corpus of 58 collected examples from online journalism, graphic design, comics, business, art, and visualization research. Our analysis highlights visual and interactive devices that support storytelling
with data, and we identify distinct genres of visualization using narrative structures such as the martini glass, interactive slideshow, and
drill-down story. In particular, we note a central concern in the design of narrative visualizations: the balance between author-driven


SEGAL AND HEER: NARRATIVE VISUALIZATION: TELLING STORIES WITH DATA 1147



elements—providing narrative structure and messaging—and readerdriven elements—enabling interactive exploration and social sharing.
These results help identify successful design practices. By explicitly
naming effective techniques (e.g., “tacit tutorials”, “semantic consistency”, “matching on content”) we hope to facilitate their reuse.
Narrative visualizations differ in important ways from traditional
forms of storytelling. In journalism, one presents related material and
sources together in a “block progression” to have clear and logical
transitions, and digresses “often, but not for long” [2]. Interactive stories present difficulties for these recommendations, as giving narrative
control to the reader permits lengthy unordered digressions. The design structures we identify help counter these pitfalls. Generalizing
across our examples, data stories appear to be most effective when
they have constrained interaction at various checkpoints within a narrative, allowing the user to explore the data without veering too far
from the intended narrative. That said, further exploration of transitions between author- and reader-driven elements presents an exciting
area for researchers and practitioners.
Our analysis also helps identify under-explored regions of the design space. For example, the “magazine style” genre is the most common genre for static visualizations, but has not been as richly utilized
with interactive visualizations. How might multiple media be better
integrated for storytelling? For example, a martini glass structure for
a visualization may be weaved into a text story: static images might
first support the text and introduce the visualization; an embedded interactive visualization may appear later, perhaps with links in the text
setting visualization parameters to highlight points made within the
prose; finally, at the article’s end, the visualization may open up to
enable free exploration. Likewise, our data shows that interactivity is
not yet common in flowcharts, comics, or videos, and that few visualizations currently use tacit tutorials or stimulating default views. In
this manner, our framework facilitates reasoning about novel juxtapositions of genres and narrative devices.
As our understanding of narrative visualization improves, it also
opens up new opportunities for visualization tool research. How
should we extend visual analysis applications to enable storytelling?
Interfaces that combine visualization construction with the specification of narrative structure, textual/graphical annotation, visual highlighting techniques, transitions, and interactive controls could have a
transformative impact on the medium, so long as they can be used by
data domain experts, not just technology experts. We believe that our
results identify important features for these future tools. By identifying recurring design patterns, we hope to help catalyze novel tools and
explorations of narrative visualization.
However, we must acknowledge that we are not experts in the study
of narrative. Rather, we are visualization designers and technologists
seeking to better understand the potential of the medium. Inevitably,
there is much that remains to be understood. For instance, what mix
of author-driven and reader-driven elements is best for different purposes? How does this vary based on the data at hand, the desired story
form, and the audience? How critical is it to provide either explicit instruction or tacit tutorials to introduce interactive features? Will these
elements become less necessary as viewers become more accustomed
to narrative visualization? The topic is ripe for future work, and would
further benefit from the input of artists, educators, and journalists.
By investigating the narrative devices used in a corpus of visualizations, our analysis has focused primarily on the design decisions made
by visualization creators. A promising direction for future research is
to focus squarely on readers’ experiences when viewing and interacting with narrative visualizations. Eye-tracking studies of newspaper
reading [11, 16] have found that readers regularly skim by scanning
graphics, headlines, and initial paragraphs before intermittently stopping to read an article. Based on these results, Garcia & Stark [11] define newspaper design as the challenge _“to give readers material that_
_is worthy of their scan, that makes them stop scanning and start read-_
_ing.”_ How do such behaviors apply to visualization? Further research
is needed to characterize how readers perceive narratives presented via
visualizations. Such studies could provide insights for design, such as
how viewers might best “skim” a narrative visualization.



A related topic is reader engagement. The examples we analyzed
tended to have “hard leads”—brief summaries describing the content
of the visualization—whereas journalism often adopts more mysterious leads [2] to promote engagement. How can “stimulating default
views” for visualizations best capture readers’ attention and personally engage them in the world of the narrative? Moreover, narrative
visualizations put data at the forefront of storytelling, yet others [2, 7]
have noted that a myopic focus on data may be a stumbling block to
narrative flow and reader engagement. The strategies discussed above
suggest ways to incorporate statistics in concert with narrative, potentially enhancing readers’ engagement with data. As Blundell [2]
notes, _“We’re supposed to be tellers of tales as well as purveyors of_
_facts. When we don’t live up to that responsibility we don’t get read.”_


**A** **CKNOWLEDGMENTS**

The authors thank Sarah Cohen, Len de Groot, Andrew Haeg, Geoff
McGhee, and anonymous reviewers for their constructive feedback.


**R** **EFERENCES**


[1] H. Beyer and K. Holtzblatt. _Contextual Design: Defining Customer-_
_Centered Systems_ . Morgan Kaufmann, 1998.

[2] W. E. Blundell. _The Art & Craft of Feature Writing_ . Plume, 1988.

[3] D. Bordwell and K. Thompson. _Film Art: An Introduction_ . McGraw-Hill,
2003.

[4] S. Buttry. The Elements and Structure of Narrative. http://www.
notrain-nogain.org/train/Res/write/sbnar.asp,
2010.

[5] J. Campbell. _The Hero with a Thousand Faces_ . New World Library, 1949.

[6] K. Cukier. Show Me: New ways of visualising data. http://www.
economist.com/node/15557455, 2010.

[7] L. Danzico. Telling stories using data: An interview with Jonathan Harris.
http://bit.ly/jh-int, 2008.

[8] R. Eccles, T. Kapler, R. Harper, and W. Wright. Stories in geotime. In
_IEEE VAST_, pages 19–26, 2007.

[9] P. Farhi. CNN hits the wall for the election. http://bit.ly/
cnn-wall, 2008.

[10] Gapminder. http://www.gapminder.org, 2010.

[11] M. R. Garcia and P. Stark. _Eyes on the News_ . The Poynter Institute, 1991.

[12] N. Gershon and W. Page. What storytelling can do for information visualization. _Commun. ACM_, 44(8):31–37, 2001.

[13] J. Heer, J. Mackinlay, C. Stolte, and M. Agrawala. Graphical histories
for visualization: Supporting analysis, communication, and evaluation.
_IEEE Trans. Vis. and Comp. Graphics_, 14(6):1189–1196, 2008.

[14] J. Heer and G. G. Robertson. Animated transitions in statistical data
graphics. _IEEE Trans. Vis. and Comp. Graphics_, 13(6):1240–1247, 2007.

[15] J. Heer, F. B. Vi´egas, and M. Wattenberg. Voyager and voyeurs: Supporting asynchronous collaborative information visualization. In _Proc. ACM_
_CHI_, pages 1029–1038, 2007.

[16] K. Holmqvist, J. Holsanova, M. Barthelson, and D. Lundqvist. Reading
or scanning? a study of newspaper and net paper reading. In J. R. Hy¨on¨a
and H. Deubel, editors, _The Mind’s Eye: Cognitive and Applied Aspects_
_of Eye Movement Research_, pages 657–670. Elsevier, 2003.

[17] L. Itti and C. Koch. Computational modeling of visual attention. _Nature_
_Reviews Neuroscience_, 2(3):194–203, 2001.

[18] G. Kress and T. van Leeuwen. _Reading Images: The Grammar of Visual_
_Design_ . Routledge, 1996.

[19] S. McCloud. _Understanding Comics_ . Kitchen Sink Press, 1993.

[20] S. McCloud. _Making Comics_ . Harper, 2006.

[21] G. Polti. _The thirty-six dramatic situations_ . The Editor Company, 1916.

[22] Tableau Public. http://tableausoftware.com/public, 2010.

[23] A. M. Treisman and G. Gelade. A feature-integration theory of attention.
_Cognitive Psychology_, 12(1):97–136, 1980.

[24] B. Tversky, J. Heiser, S. Lozano, R. MacKenzie, and J. Morrison. Enriching animations. In R. Lowe and W. Schnotz, editors, _Learning with_
_animation_ . Cambridge University Press, 2007.

[25] F. B. Vi´egas, M. Wattenberg, F. van Ham, J. Kriss, and M. McKeon.
Many Eyes: a site for visualization at internet scale. _IEEE Trans. Vis. and_
_Comp. Graphics_, 13(6):1121–1128, 2007.

[26] C. Ware. _Information visualization: perception for design_ . Morgan Kaufmann, San Francisco, CA, 2004.

[27] W. Wojtkowski and W. G. Wojtkowski. Storytelling: its role in information visualization. In _European Systems Science Congress_, 2002.


1148 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 16, NO. 6, NOVEMBER/DECEMBER 2010



**A** **PPENDIX** **: N** **ARRATIVE** **V** **ISUALIZATION** **E** **XAMPLES**


[1] E. Cadora and L. Kurgan. Architecture and Justice (Brooklyn Crime Blocks).
Columbia University’s Spatial Information Design Lab, 2006. http://www.
spatialinformationdesignlab.org/MEDIA/PDF_04.pdf.

[2] E. Tufte. John Snow’s Chart of Deaths from Cholera. Visual Display of Quantitative
Information, 2001.

[3] E. Tufte. Politicians Abuse their Free-mailing Privileges before Elections. Visual
Display of Quantitative Information, 2001.

[4] S. Rosenthal. Football Drawings. Visual Complexity. http://www.
susken-rosenthal.de/fussballbilder/indexen.html.

[5] T. Laureyssens. Pedestrians Crossing the Street. Unknown, 2005.
http://www.visualcomplexity.com/vc/project_details.
cfm?id=255&index=7&domain=Pattern%20Recognition.

[6] W. Andrews, A. Cypress, J. Kazil, T. Lindeman, and K. Yourish. The Climate
Agenda. The Washington Post. http://www.washingtonpost.com/
wp-srv/special/climate-change/global-emissions.html?ad=

inw.

[7] C. Wilson. When Did Your County’s Jobs Disappear? The Washington Post/Slate,
2009. http://www.slate.com/id/2216238/?ad=ins.

[8] Acadametrics House Price Index. Financial Times. http://www.
acadametrics.co.uk/house_prices_June10.swf.

[9] S. Wheeler and S. Bernard. Banks’ Earnings: How Compensation Relates to
Performance. Financial Times, 2010. http://www.ft.com/cms/s/0/

4ce7a094-1c9e-11df-8456-00144feab49a.html.

[10] H. Warrell, C. Jones, and J. Thompson. Deadly Offensive: Taliban Attacks
in Pakistan. Financial Times, 2009. http://www.ft.com/cms/s/0/

1ae86218-b993-11de-abac-00144feab49a.html.

[11] R. Birkett. GDP Moves by Sector. Financial Times, 2010. http://www.ft.
com/cms/s/0/14cc2e70-04e6-11df-9a4f-00144feabdc0.html.

[12] V. Bevins and R. Birkett. UK Economic Data. Financial Times, 2010. http://www.ft.com/cms/s/0/

bd7b628c-2068-11df-bf2d-00144feab49a.html.

[13] P. Allen, J. Ridley, and C. Levene. Budget 2010: Reaction from around the
UK. Guardian, 2010. http://www.guardian.co.uk/uk/interactive/
2010/mar/24/budget-2010-case-studies-map.

[14] P. Allen. Formula One 2010: Driver’s Rankings. Guardian, 2010.
http://www.guardian.co.uk/sport/interactive/2010/feb/
02/formula1-championship-points-2010.

[15] C. Oliver and M. Wainwright. Lighting Up Hadrian’s Wall. Guardian,
2010. http://www.guardian.co.uk/culture/interactive/2010/
mar/12/hadrians-wall-lights-500-torches.

[16] Mapping Hydropower Hotspots across the UK. Guardian, 2010.
http://www.guardian.co.uk/environment/interactive/
2010/mar/09/map-hydropower-hotspots-uk.

[17] P. Allen. Moscow Metro Bombs: Interactive Map. Guardian, 2010.
http://www.guardian.co.uk/world/interactive/2010/mar/
29/moscow-metro-bombs-terror-map.

[18] C. Oliver. The World Economy Turns the Corner. Guardian, 2010.
http://www.guardian.co.uk/business/interactive/2010/
jan/26/recession-gdp.

[19] J. Heer, A. Haeg, and M. Agrawala. Minnesota Employment Explorer. Minnesota
Public Radio, 2007. http://minnesota.publicradio.org/projects/
2008/07/16_minnesota_slowdown/.

[20] L. Byron, A. Cox, and M. Ericson. A Map of Olympic Medals. The New York
Times, 2008. http://www.nytimes.com/interactive/2008/08/04/
sports/olympics/20080804%_MEDALCOUNT_MAP.html.

[21] M. Bloch, S. Carter, A. Cox, and J. Ward. All of Inflation’s Little Parts. The New
York Times, 2008. http://www.nytimes.com/interactive/2008/
05/03/business/20080403_SPENDING_GRAPHIC.html.

[22] S. Carter and A. Cox. Paths to the Top of the Home Run Charts. The New York
Times, 2007. http://www.nytimes.com/ref/sports/20070731_

BONDS_GRAPHIC.html.

[23] M. Bloch, L. Byron, S. Carter, and A. Cox. The Ebb and Flow of
Movies: Box Office Receipts 1986-2008. The New York Times, 2008.
http://www.nytimes.com/interactive/2008/02/23/movies/
20080223_REVENUE%_GRAPHIC.html.

[24] S. Carter, A. Cox, and K. Quealy. The Jobless Rate for People Like You.
The New York Times, 2009. http://www.nytimes.com/interactive/
2009/11/06/business/economy/unemployment-lines.html.

[25] Advertisement: Bus. United Technology. http://www.pewclimate.org/
docUploads/UTC_fuel_cell%20ad_0.pdf.

[26] Advertisement: Helicopter. United Technology. http://farm4.static.
flickr.com/3030/2572980233_0339ee260a.jpg.

[27] N. V. Kelso, M. Lebling, K. Yourish, R. O’Neil, W. Andrews, J. Kazil, T. Lindeman,
L. Shackelford, and P. Volpe. Analyzing Obama’s Schedule. The Washington Post,
2010. http://projects.washingtonpost.com/potus-tracker/

?ad=inw.

[28] X. Brooks and C. Oliver. Oscars 2010: The Best Picture Nominees. Guardian, 2010.
http://www.guardian.co.uk/film/filmblog/interactive/
2010/mar/03/oscars-2010-best-picture-nominees.

[29] P. Allen. The Consumer and Retail Price Indices since 2006. Guardian, 2010.
http://www.guardian.co.uk/business/interactive/2009/
mar/24/rpi-inflation.

[30] P. Allen, J. Glover, and W. Woodward. UK Voting Intentions. Guardian, 2010.



http://www.guardian.co.uk/politics/interactive/2009/
jan/26/icm-polls-uk-voting-intention.

[31] A. Cox, X. G.V., and D. Leonhardt. Comparison of Bear Markets. The New York
Times, 2008. http://www.nytimes.com/interactive/2008/10/11/
business/20081011_BEAR_MARKETS.html.

[32] G. Dance, A. Pilhofer, A. Lehren, and J. Damens. Faces of the Dead. The
New York Times, 2010. http://www.nytimes.com/interactive/us/

faces-of-the-dead.html.

[33] S. Carter, A. Cox, K. Quealy, and A. Shoenfeld. How Americans Spend their Day.
The New York Times, 2009. http://www.nytimes.com/interactive/
2009/07/31/business/20080801-metrics-graphic.html?ref=

multimedia.

[34] G. Dance and E. Goodridge. Michelle Obama’s Family Tree. The New York
Times, 2009. http://www.nytimes.com/interactive/2009/10/
08/us/politics/20091008-obama-family-tree.html?ref=

multimedia.

[35] M. Bloch, A. Cox, J. C. McGinty, and K. Quealy. Netflix Rentals. The New York
Times, 2010. http://www.nytimes.com/interactive/2010/01/10/
nyregion/20100110-netflix-map.html?ref=multimedia.

[36] Steroids or Not, the Pursuit is On. The New York Times, 2006.

[37] S. Carter, M. Ericons, and J. Ward. Vancouver’s Olympic Venue. The New
York Times, 2010. http://www.nytimes.com/interactive/2010/
02/09/sports/olympics/2010-olympics-venue-map.html?ref=

multimedia.

[38] K. Downs, B. Harden, L. Heron, L. Karklis, and F. Uenuma. On
the Map: Five Major North Korean Prison Camps. The Washington
Post. http://www.washingtonpost.com/wp-srv/special/world/
north-korean-prison-camps-2009/?ad=inw.

[39] S. Anderson, G. Calabro, and M. H. andRyan Thornburg. Spheres of Influence: The Bush Campaign Pioneers. The Washington Post, 2004.
http://www.washingtonpost.com/wp-srv/politics/pioneers/
pioneers_spheres.html.

[40] J. Bachman. A Visual Guide to the Financial Crisis. Flowing Data, 2008. http://flowingdata.com/2008/11/25/
visual-guide-to-the-financial-crisis/.

[41] P. S. Ng. Economic Meltdown of 2008-2009. Flowing Data, 2008. http://bit.
ly/SBAAb.

[42] E. Klimiuk. Where Did All the Money Go? Flowing Data, 2008. http://bit.
ly/SBAAb.

[43] E. Tufte. Life Cycle of a Beetle through a Year. Visual Display of Quantitative
Information, 2001.

[44] S. McCloud. Making Comics, 2006.

[45] M. Green, H. Warrell, S. Tarling, S. Bernard, and M. Formentini. Afghanistan:
Behind the Front Line. Financial Times, 2009. http://www.ft.com/cms/s/
0/663b649e-b7e6-11de-8ca9-00144feab49a.html.

[46] J. Soble. Toyota Timeline: A Company History. Financial Times, 2010. http://www.ft.com/cms/s/0/

1f8f077c-2301-11df-a25f-00144feab49a.html.

[47] Gapminder. Gapminder Human Development. Gapminder, 2005. http://www.
gapminder.org/downloads/human-development-trends-2005/.

[48] P. Allen. Earthquakes: Why They Happen. Guardian, 2010. http:
//www.guardian.co.uk/world/interactive/2008/jan/23/
earthquakes.

[49] G. N. Guardian Science Team. Iran’s Nuclear Programme. Guardian, 2010. http:
//www.guardian.co.uk/world/interactive/2003/jun/19/iran.

[50] Shaun White’s Double McTwist. Guardian, 2010. http://
www.guardian.co.uk/sport/interactive/2010/feb/19/
winterolympics2010-vancouver.

[51] P. Allen and G. News. Toyota’s Stick Accelerator Problem. Guardian, 2010.
http://www.guardian.co.uk/business/interactive/2010/
feb/04/toyota-automotive-industry.

[52] J. Ward, S. Carter, G. Roberts, X. G. V., M. Gr¨ondahl, K. Quealy, and A. Cox.
Alpine Skiing, from Technical Turns to Tucks and Speed. The New York
Times, 2010. http://www.nytimes.com/interactive/2010/02/20/
sports/olympics/downhill-overview.html?ref=multimedia.

[53] A. Cox. Budget Forecasts vs. Reality. The New York Times, 2010.
http://www.nytimes.com/interactive/2010/02/02/us/
politics/20100201-budget-porcupine-graphic.html.

[54] K. Quealy, G. Roth, and R. Schneiderman. How the Government
Dealt with Past Recessions. The New York Times, 2009. http:
//www.nytimes.com/interactive/2009/01/26/business/
economy/20090126-recessions-graphic.html.

[55] Mac Orientation Video. Apple. http://www.apple.com/findouthow/
mac/#anatomy.

[56] Delta Airplane Safety Video. Delta Airlines, 2008. http://www.youtube.
com/watch?v=MgpzUo_kbFY.

[57] A. Leonard. The Story of Stuff. Story of Stuff Project, 2008. http://www.
storyofstuff.com/.

[58] W!LDBRAIN. Virgin America Airplane Safety Video. Virgin America,
2007. http://www.youtube.com/watch?v=eyygn8HFTCo&feature=

channel.


