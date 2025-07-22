[Visual Informatics 3 (2019) 27–37](https://doi.org/10.1016/j.visinf.2019.03.004)


[Contents lists available at ScienceDirect](http://www.elsevier.com/locate/visinf)

# Visual Informatics


[journal homepage: www.elsevier.com/locate/visinf](http://www.elsevier.com/locate/visinf)

# Interactive map reports summarizing bivariate geographic data


Shahid Latif [∗], Fabian Beck


_University of Duisburg–Essen, paluno – The Ruhr Institute of Software Technology, Germany_



a r t i c l e i n f o


_Article history:_
Received 10 December 2018
Received in revised form 8 February 2019
Available online 21 March 2019


_Keywords:_
Geographic visualization
Natural language generation
Interactive documents


**1. Introduction**



a b s t r a c t


Bivariate map visualizations use different encodings to visualize two variables but comparison across
multiple encodings is challenging. Compared to a univariate visualization, it is significantly harder
to read regional differences and spot geographical outliers. Especially targeting inexperienced users
of visualizations, we advocate the use of natural language text for augmenting map visualizations
and understanding the relationship between two geo-statistical variables. We propose an approach
that selects interesting findings from data analysis, generates a respective text and visualization, and
integrates both into a single document. The generated reports interactively link the visualization
with the textual narrative. Users can get additional explanations and have the ability to compare
different regions. The text generation process is flexible and adapts to various geographical and
contextual settings based on small sets of parameters. We showcase this flexibility through a number
of application examples.
© 2019 Zhejiang University and Zhejiang University Press. Published by Elsevier B.V. This is an open access
[article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by-nc-nd/4.0/).](http://creativecommons.org/licenses/by-nc-nd/4.0/)



The interplay of two variables reveals how one entity potentially influences the other. In a geographic context, this influence may depend on the geography of the region. For instance,
storms might cause more fatalities in densely populated areas.
Standard map visualizations such as heatmaps, choropleths, and
cartograms are designed to visualize one numerical variable at a
time. The visualization of two geo-statistical variables on maps
is more challenging. To simultaneously visualize two variables,
a combination of two univariate maps can be overlaid, for instance, the first variable shown as a choropleth map and the
second variable encoded in sizes of overlaid shapes; alternatively,
separate views can be used. However, especially inexperienced
users might face problems interpreting the bivariate visualization
correctly and effectively. Users with a low visualization literacy
might have problems understanding the respective visualization.
And even users with more experience might find it hard to detect
spatial patterns and spot outliers. Hence, there is a need to make
bivariate geo-statistical visualizations more self-explaining and
guide users through data analysis.

When a visualization is not fully self-explaining, we can add
text in the form of captions and annotations to it. Also, to describe
the results of data analysis, textual representations can easily


∗ Corresponding author.
_E-mail addresses:_ [shahid.latif@paluno.uni-due.de (S. Latif),](mailto:shahid.latif@paluno.uni-due.de)
[fabian.beck@paluno.uni-due.de (F. Beck).](mailto:fabian.beck@paluno.uni-due.de)


Peer review under responsibility of Zhejiang University and Zhejiang
University Press.



guide a reader through important findings. Hence, we believe
that augmenting a bivariate map visualization with a textual
report and interactively linking both can significantly improve
users’ abilities to understand the data. Using natural language
generation technology, we could easily develop a joint automatic
generation of the visualization and an accompanying text for a
specific type of applications (e.g., reports of fatalities). However,
we want to find more generalizable solutions that can deal with
various types of geo-statistical variables (e.g., fatalities, monetary,
demographic). Whereas visualizations are usually generalizable
to different scenarios already, automatically produced text heavily depends on domain vocabulary and context. In contrast, we
propose a text generation process that is flexible and adaptable
to different variable types and geographic settings. This flexibility is achieved through a set of parameters providing metadata
and context. The parameters also influence the visual encoding.
Text and visualization are finally presented together in a linked
interactive representation.

We developed _interactive Map Reports_ (iMR), a Web-based
tool that automatically generates a narrative and visualization
to describe the analysis results for bivariate geo-statistical data.
The sample shown in Fig. 1 explains fatalities caused by storm
events in the USA, 2017. The reports summarize noteworthy
patterns and relationships among the variables. In addition, they
provide explanations on selected regions and the ability to compare any two regions of interest on demand. The color and shape
encodings of variables in the text help establish quick linking
of respective regions across both representations. To generate
the reports, we combine data analysis techniques with natural language generation and interactive visualization. Our main
scientific contributions are:



[https://doi.org/10.1016/j.visinf.2019.03.004](https://doi.org/10.1016/j.visinf.2019.03.004)
2468-502X/ © 2019 Zhejiang University and Zhejiang University Press. Published by Elsevier B.V. This is an open access article under the CC BY-NC-ND license
[(http://creativecommons.org/licenses/by-nc-nd/4.0/).](http://creativecommons.org/licenses/by-nc-nd/4.0/)


28 _S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_


**Fig. 1.** A map report describing the loss of lives due to storms in the USA during 2017. The map visualization uses two different encodings to visualize a _focus_ and a
_context_ variable. The narrative (right column) provides an overview of the data analysis. Graphics in the text help establish linking between the two representations.
Users can get additional details on a selected region or on a comparison of two selected regions (dashed rectangles).




 - an automatic detection and selection of relevant information

from bivariate geo-statistical data (Section 3),

 - a versatile template-based text generation technique to pro
duce a narrative adaptable to different contextual scenarios
(Section 4),

 - an adaptable method to produce map reports for various ge
ographical regions and granularity consisting of interactively
linked narrative and visualizations (Section 5), and

 - a demonstration of generalizability of the approach in vari
ous application scenarios (Section 6).


[The interactive system (iMR) is available at https://vis-tools.](https://vis-tools.paluno.uni-due.de/imr)
[paluno.uni-due.de/imr and the supplemental material contains](https://vis-tools.paluno.uni-due.de/imr)
an interactive appendix having additional examples.


**2. Related work**


We explore the existing literature from two different
perspectives—techniques for visualizing bivariate statistical data
on maps and the approaches that use a combination of text and
visualizations for communicating the results of the analysis.

Thematic maps are used to visualize variations in values of
a variable across geographical space. The variable is mostly encoded as colors (Brewer et al., 1997), sizes and shapes of the
geographical regions (cartograms), or specific symbols overlaid on
top of the map (Flannery, 1971). Although most of the thematic
maps are used to visualize a single variable (e.g., choropleths,
heatmaps), there exist techniques that generalize this concept
to bivariate (Howard and MacEachren, 1996; Brewer and Campbell, 1998) and multivariate data (Kim et al., 2013). A taxonomy
of bivariate map types can be found in Elmer’s work (Elmer,
2012, Figure 2.1). This classification is based on various combinations of visual variables and is adapted from the work of Nelson
(2000), MacEachren (2004). According to (Elmer, 2012), although
there are more than eleven different types (identified from six
cartography books (Elmer, 2012, Table 2.1)) of bivariate map



types, only two (bivariate choropleths and choropleths with overlaid graduated symbols) have been generally used in previous
literature. Bivariate map visualizations, by construction, are visually more complex and harder to comprehend in comparison to
their univariate counterparts. To facilitate the analysis of relationships among variables in geographical setting, Monmonier (1990)
combines spatial representation with visual statistical summaries
(scatter plot matrix). In contrast, we advocate textual explanations that make the visualizations self-explaining and provide
an anchor point to explore the information specifically to users
lacking visualization literacy.

The automatic generation of written narratives from data and
other abstracted information falls under the scope of Natural Language Generation (NLG) (Deemter et al., 2005; Reiter et al., 2000;
Gatt and Krahmer, 2018). Commercial tools such as _Wordsmith_
and _Arria NLG Studio_ allow for building customizable templates
for text generation and use an advanced grammar model to do the
grammar related tasks (e.g., subject–verb agreement). However,
in these systems, users have to construct templates for each
application or dataset. In contrast, we aim at generalizing the
template-based text generation approach to different contexts by
using a minimalistic set of parameters.

Most of the existing approaches generate natural language text
for non-geographic data; only a few have addressed geographical
data. Among these, Dale et al. (2005) generate route descriptions
of paths constructed from the Geographical Information System
datasets. Ramos-Soto et al. (2015) produce weather forecast reports. Thomas and Sripada (2007) provide (audio) summaries
of geo-referenced data for better conveying information to the
visually impaired population. Turner et al. (2008) present road
ice weather forecasts by taking into account geographic features
such as altitude, direction, population, etc. A very recent system, _SafeDrive_ (Braun et al., 2018), provides the textual feedback
on driving style of drivers to improve driving habits. The work
of Molina et al. (2015) is close to ours as they produce descriptions of geographically distributed hydrological sensor data


_S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_ 29



alongside a map. While their system includes a geographical
map with the possibility to get temporal distributions of individual sensor readings, the textual and graphical representations
are not interactively linked. Furthermore, the major focus of
these approaches is on NLG and the text generation process is
data dependent which makes them hard to generalize to other
datasets.

Among the many other existing text generation approaches
(Gatt and Krahmer, 2018), only a few discuss the generation of
text in combination with visualizations. They are spread across
many different domains, for instance, generation of instruction
manuals for simple machines (Wahlster et al., 1993), health care
data reporting (Jain and Keller, 2015; Hunter et al., 2008), performance analysis of participants in virtual learning environment (Ramos-Soto et al., 2017), scuba diver’s profiling (Sripada
and Gao, 2007), and description of the execution behavior of a
program (Beck et al., 2017). Other approaches have discussed the
automatic technical summarization of already generated graphical content (Mittal et al., 1995; Demir et al., 2012; Hullman et al.,
2013). These systems focus on the explanatory aspect of data
analysis and do not offer much explorability.

More recent approaches show that the interlinking of text and
visualization can facilitate users in the visual exploration of data.
For instance, _Voder_ (Srinivasan et al., 2019) uses automatically
generated textual descriptions about the visualized data as interactive links to suggest other relevant types of visualizations
for better understanding. Kwon et al. (2014) suggest animating
corresponding parts of a visualization (e.g., parallel coordinates)
on interacting with the relevant text. But here the text is written
by a human expert and not automatically generated. _VIS Author_
_Profiles_ (Latif and Beck, 2019) combines generated text and visualizations in an interactive document offering both explanatory
and exploratory aspect of data analysis. However, the focus of
_VIS Author Profiles_ and other discussed approaches is narrow and
they are tailored for specific applications and are not easy to be
generalized for different contexts and datasets. In comparison,
our focus is broader and the presented approach generalizes to
different contextual settings.

Besides the interactive linking of text and visualizations, the
use of word-sized graphics or sparklines (Tufte, 2006) has also
been suggested for better integrating textual and visual content (Beck and Weiskopf, 2017; Goffin et al., 2014). In this paper,
we use filled circles in line with text to better connect it with the
map visualization as shown in Fig. 1.


**3. Content selection**


Any natural language generation begins with content determination, which decides on what information would be conveyed (Reiter et al., 2000). Before delving into the details of data
analysis, we first introduce our target dataset and the results of
an explorative study aimed at getting an initial overview of the
possible content.


_3.1. Bivariate geo-statistical data_


We are focusing on the analysis of bivariate geo-statistical
data—measurements of two numerical variables for a geographic
region. Particularly relevant are those scenarios where one variable potentially influences the other. For instance, life expectancy
might depend on the amount of health expenditure. Similarly,
intensity and number of storms can influence the number of lives
lost. In the following, we refer to the variable that potentially
depends on the other as the _focus_ variable and the other as the
_context_ variable. If a causality can be assumed (e.g., because it is
obvious or there exists a reasonable explanation for it), it points



from _context_ to _focus_ variable. In our analysis, we use three levels
of geography, namely regions (e.g., USA), groups of subregions
(e.g., group of states), and subregions (e.g., individual states). We
use the storm–death dataset as our running example.


_3.2. Explorative study_


To get an initial overview of what aspects to consider while
describing bivariate geo-statistical data, we conducted an explorative study with two participants (P1, P2). Both participants
were Ph.D. students working in the field of visualization but
were not involved in this project. They were presented with an
interactive version of a bivariate map visualization as shown in
Fig. 2, similar to the ones later used in our interactive system. In
these visualizations, the _focus_ variable was encoded in the radius
of filled circles placed on top of the choropleth map showing the
_context_ variable.

The participants were asked to summarize the visualization
(Task I), describe one particular subregion (Task II), and provide
a comparative view of two given subregions (Task III). They had
the possibility to write as much text as they wanted and there
was no time limit.

_Task I—Summary:_ Both participants began with the description
of the subregions having minimum and maximum values of the
_focus_ variable followed by the explanation of outlying regions. P1
included information on a possible correlation between the variables. P2 described spatial trend of the context variable. Finally,
both participants noticed and described abrupt changes of values
between neighboring subregions.

_Task II—Region-specific description:_ P1 described the values of
both variables for the given subregion, followed by naming the
other regions that show similar behavior, whereas P2 provided
a comparison with the mean values. Further, P2 also highlighted
a specific subregion that has higher values of the _context_ variable
compared to its direct neighbors.

_Task III—Comparison:_ Both participants compared the values
of each variable for two regions and described them in a single
sentence. P1 included more details about one subregion as one of
the subregions presented to him for comparison was an outlier.

The results show that the prominent aspects are the reporting of outliers (univariate and bivariate), comparisons of regions
with their neighbors, variations of variable values across space,
and subregions showing similar behavior. In addition, a correlation and variations of values across different subregional levels
(e.g., parts of Europe) might reveal interesting patterns and are
worth reporting. For instance, in Fig. 2 (left), the correlation is
much stronger in the Southern states ( _ρ_ = 0 _._ 753) compared to
the overall correlation for the country ( _ρ_ = 0 _._ 400).


_3.3. Data analysis_


Next, we discuss statistical approaches to automatically identify the content that will be part of our narrative. In contrast to
basic information such as ranges of variable values, correlations
among variables, and extreme values, the detection of univariate
outliers, bivariate outliers, and regional differences requires more
sophisticated data analysis approaches.


_3.3.1. Univariate outliers_

The importance of extreme values (minimum and maximum)
in a dataset varies depending on the distribution of variables. A
Tukey’s boxplot (Tukey, 1977) uses measures namely, the first
quartile ( _Q_ 1), median ( _Q_ 2), third quartile ( _Q_ 3), and interquartile range ( _IQR_ = _Q_ 3 − _Q_ 1) to describe a univariate distribution. Hoaglin et al. (2000) categorize the observations smaller


30 _S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_


**Fig. 2.** Bivariate map visualizations used in the explorative study. (Left, P1) Deaths caused by storms in various states of the USA. (Right, P2) Average life expectancy
and health expenditures across Europe.



than _Q_ 1 − 1 _._ 5 - _IQR_ or larger than _Q_ 3 + 1 _._ 5 - _IQR_ as the potential candidates for outliers. Although somewhat arbitrary, this threshold
for detecting outliers works well based on their experience with
many datasets.

We analyze each variable individually and identify the univariate outliers i.e., the points lying outside [ _Q_ 1 − 1 _._ 5 - _IQR_ _,_ _Q_ 3 + 1 _._ 5 _IQR_ ] range. Fig. 3 shows the distribution and outliers corresponding to each of the two variables in our exemplary dataset.


_3.3.2. Bivariate outliers_

We are also interested in subregions that demonstrate different behavior compared to the rest of the subregions based
on the values of both variables. Such a bivariate outlier may
not necessarily be an outlier in both of the univariate variables.
For instance, although the states of Nevada and Florida in Fig. 3
(marked with red dots) are not outliers in variable _storms_, they
are bivariate outliers as shown by the bagplot in Fig. 4. A bagplot (Rousseeuw et al., 1999) is a bivariate generalization of
a boxplot and visualizes the distribution, spread, and outliers
jointly for both variables. Three main components of a bagplot
are: the _bag_ containing 50% of the observations, the _fence_ usually
obtained by inflating the bag by a factor of 3 separating inliers
from outliers, and the _loop_, that is the convex hull of the points
lying between the bag and the fence.

The detection of bivariate outliers depends on the shape or
distribution of the data, which is often characterized by a covariance matrix. For identifying the outliers, we use a well-known
distance measure, the Mahalanobis distance, which takes into
account the covariance matrix and is defined as the distance

between an observation and a multivariate distribution. Mathematically, this distance is specified as:

_d_ = ~~√~~ ( _x_ − _µ_ ) _[T]_ _S_ [−] [1] ( _x_ − _µ_ ) (1)


where _x_ = ( _x_ 1 _,_ _x_ 2 ) is the vector of variables, _µ_ = ( _µ_ 1 _, µ_ 2 ) is the
vector of means and _S_ is a two-dimensional symmetric covariance
matrix. The resulting value _d_ represents the Mahalanobis distance
of point _x_ from the mean _µ_ of the distribution.

For a constant value of _d_, Eq. (1) defines a two-dimensional
ellipsoid centered at _µ_ . The probability of ellipsoid follows a _χ_ [2]

distribution with _p_ degrees of freedom (Härdle and Simar, 2007).
Therefore, the ellipsoid satisfying


( _x_ − _µ_ ) _[T]_ _S_ [−] [1] ( _x_ − _µ_ ) ≤ _χ_ _p_ [2] [(] _[α]_ [)] (2)


has a probability of 1 − _α_ . Hence, for _p_ = 2 (bivariate case) and
_α_ = 0 _._ 5 ⇒ _χ_ [2] = 5 _._ 99. Eq. (2) states that any observation is
considered a bivariate outlier for which the squared Mahalanobis
distance is greater than 5.99.



_3.3.3. Geospatial trends_

The behavior of any statistical variable can vary considerably
depending on the geographical subregion. For instance, Fig. 1
shows that the coastal states of the USA have experienced a
higher number of storms, and as a consequence, more casualties.
To identify this behavior, we take a regional subdivision of the
overall shown geographic region under consideration. The United
Nations (1999) provides a classification of the countries of the
world into groups. For instance, European countries are grouped
into Eastern, Western, Northern, and Southern countries. Similarly, the regional classification of the USA discerns West, Midwest, Northeast, and South. Using this grouping (or other externally provided groupings), we can look for differences between
these groups. In particular, we detect if there is a strong positive
or negative correlation between _focus_ and _context_ variable in
one or more of these groups. Besides the bivariate outliers, an
identification of subregions that show different behavior compared to the adjacent subregions can be of interest. For instance,
Fig. 1 shows that the state of Nevada has different statistics
with respect to both variables compared to its neighboring states,
Arizona, California, Idaho, Oregon, and Utah. To this end, we
compare the values of each variable for every subregion with its
neighbors to identify the regions showing different statistics.


**4. Text generation**


In contrast to advanced text generation approaches based on
a grammar model or machine learning (Gatt and Krahmer, 2018),
we use a template-based text generation approach because of its
good applicability and sufficient flexibility. Deemter et al. (2005)
provide an in-depth comparison of generation approaches.


_4.1. Templates to narrative_


Having selected the content, the next step is to transform this
information into a written narrative that consists of paragraphs
containing interconnected sentences. To this end, we use a similar
approach for controlling the sequence of the generated phrases
and sentences as described in _Method Execution Reports_ (Beck
et al., 2017) and _VIS Author Profiles_ (Latif and Beck, 2019). Directed
acyclic decision graphs guide the generation flow and produce
text from pre-written templates. Fig. 5 shows the decision graph
that is responsible for generating the main part of our map
reports. The process begins with the _Start_ node and follows a
deterministic path until the _Stop_ node is reached. The _decision_
nodes (rounded rectangular) lead the path according to the values


_S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_ 31


**Fig. 3.** Box plots showing the distribution of _deaths_ caused by _storms_ in the USA during 2017. The dataset contains univariate outliers in both variables.


**Fig. 4.** Bagplot of _deaths_ caused by _storms_ in the USA during 2017. The _bag_ (blue) contains almost 50% of the data points, the _loop_ (light blue) including points
outside bag but inside the fence. Bivariate outliers are marked as red dots. (For interpretation of the references to color in this figure legend, the reader is referred
to the web version of this article.)



of the decision variables. The _text_ nodes (rectangular) are responsible for sentence creation and, when visited, add a new sentence
or phrase to the narrative. Any traversal from _Start_ to _Stop_ node
results in a meaningful narrative.


_4.2. Adaptable templates_


To achieve flexibility in narration and to make the template
adaptable to different datasets, we leverage user-defined parameters that describe the meta data about the scenario. Through these
parameters, we add semantics and domain-specific vocabulary
that cannot be automatically detected from the raw data. The list
of parameters along with short descriptions and possible values
is shown in Table 1. The parameters _Region_ and _Subregion Level_
define the name of the region and the name of the level of detail
for regions respectively. The parameters _Focus_ and _Context Type_
define the type of both variables that can be selected from a list
of predefined values. The choice of adjectives, quantifiers, and
verbs depends on these variable types. For instance, for the type
_casualties_, possible phrases are: _‘‘X suffered several casualties"_, _‘‘X_
_reported a large number of deaths"_, or _‘‘X lost many lives"_ . Similarly,
for the variable type _monetary_, a possible phrase could be _‘‘X spent_
_a large amount on Y"_ or _‘‘X spent less on Y"_ . Depending on the
variable type, we pick verbs from a list of synonymous verbs to
make the text more interesting to read.

In addition to the quantifiers and verbs, the choice of adverbs
(e.g., better, worst) depends on the context or situation under
consideration. We describe three possible _situations:_




 - **Positive:** situations where higher values of the _focus_ variable

are desirable. For instance, higher values of average life
expectancy are commonly considered to be desirable.

 - **Negative:** situations that favor lower values of the _focus_

variable. For example, the cities reporting less number of

fatalities occurred in road accidents would be considered as

better.

 - **Neutral:** situations that do not clearly favor small or large

values of the _focus_ variable. For instance, only depending on
a country’s situation (e.g., aging society or unemployment of
young people), lower or higher birth rates are desirable.


Combining the variable type with the _situation_, we can now use
more expressive and specific phrases to describe the results. For
_Focus Type_ ← _demographic-indicator_ and _Situation_ ← _positive_, a
possible phrase could be; _‘‘X reports better values of life expectancy_
_compared to Y"_ . Similarly, the _Context Type_ ← _incidents_ but the
_situation_ ← _negative_ could result in; _‘‘X was the safest subregion_
_due to the least number of accidents"_ .

Another consideration is the presence of a strong correlation
which may wrongly be interpreted as causal. However, correlation does not imply causality and it is not possible to automatically extract causality from the numerical data. The parameter
_Causality_ helps in avoiding wrong interpretations about causality

based on the values of correlations.


32 _S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_


**Fig. 5.** Decision graph that shows the text generation process. Round-rectangular decision nodes control the path while rectangular text nodes add a text fragment
when visited. The green path marks the narrative generation for the example in Fig. 1.


**Table 1**
User-defined parameters for configuring the map reports.


Parameter Description Values


_Region_ Name of the region for which map is displayed String value, e.g., _World_, _Europe_, _Germany_
_Subregion Level_ Name of the type of regions the map is subdivided in String value, e.g., _countries_, _states_, _cities_
_Focus/Context Type_ Variable types according to predefined categories _incidents_, _casualties_, _demographic-indicator_,
_quantitative_, _percentage_, _monetary_, or _indicator_


_Situation_ Type of situation with respect to _focus_ variable _positive_, _negative_, or _neutral_
_Causality_ If causality can be assumed from _context_ to _focus_ variable _yes_ or _no_



_4.3. Long lists of items_


During the analysis process, we need to handle long lists
of subregions, e.g., a larger number of univariate outliers. Each
member of the list is associated with a numerical value of the
variable attached. Since our final output is natural language text,
the inclusion of long lists makes the text lengthy and boring
to read. Therefore, we restrict the size of these lists. However,
instead of cutting the list to a fixed size, we use a dynamic
selection method that slices the list to have items in a given
range (Latif and Beck, 2019, Section 4.4). The list is cut at the point
where the difference to the following value is quite large.


**5. Interactive map reports**


To implement our approach, we developed _Interactive Map_
_Reports (iMR)_, a Web-based system that generates analysis reports for bivariate geo-statistical data. Fig. 1 shows the interface
of our tool and the components of the generated report. A map
visualization on the left visualizes two variables using two different encodings. The right column presents the generated narrative
consisting of an overview and additional details on the selected
subregion or a comparison of any two selected subregions (shown
below the map in Fig. 1 for space efficiency). The small info icon
indicates the availability of additional explanations—for instance,
a complete list of regions with their respective variable values
or details on the analysis methods used to phrase the respective
sentence. The use of small graphics (circles for the _focus_ and color
coding for the _context_ variable) in the text supports the quick
comparison of various regions while reading the text and also
makes it easier to find the corresponding subregion on the map.



The subregion names are produced in boldface characters and
are clickable—when clicked, the system highlights the respective
subregion on the map. A tool-tip presents the exact numerical
values of both variables when hovering over the subregions.


_5.1. Bivariate map visualization_


For visualizing bivariate geo-statistical data on a geographical map, we employed a standard technique that performed
well in a user study comparing different bivariate map visualizations (Elmer, 2012). It uses two different encodings, one for
each variable. The _context_ variable is visualized as a choropleth
map based on a single-colored linear brightness gradient. The
values of the _focus_ variable are encoded in the radii of filled circles
and are overlaid on top of the choropleth map. These circles are
positioned at the centroid of the respective subregion.

The selection of colors for encoding the _focus_ variable depends on the specified _situation_, i.e., _positive_ → green, _negative_
→ red, and _neutral_ → orange. This choice is based on the fact
that green color is generally associated with positive and safe
situations while red is considered to be a sign of warning or
danger. However, the choice of orange color for a _neutral_ situation
is somewhat arbitrary and has been chosen for better visibility as
it has to be overlaid on top of black and gray color. For the _context_
variable, we always use the same neutral gradient (light gray to
dark gray) irrespective of the _situation_ as the situation depends
only on the _focus_ variable.


_5.2. Textual summary of analysis_


The first section of the generated narrative is the _overview_ that
summarizes the results of the data analysis. This section is divided


_S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_ 33


**Fig. 6.** An interactive map report describing average life expectancy and health expenditure across Europe in 2018.



into three paragraphs. The structure and order of the paragraphs
are fixed but the sentences change considerably depending on
the dataset and scenario. In Fig. 1, the _overview_ is generated by
traversing the green path in the decision graph of Fig. 5.

The opening paragraph consists of a single sentence that introduces the dataset and the visual encodings with the help of in-line
legends. The second paragraph summarizes the results of the
univariate analysis for the _focus_ variable. It starts by stating the
average values of the _focus_ variable, followed by the range of its
values accompanied by the subregion names (text node _Vis. desc._ ).
In the case of multiple subregions having the same minimum
(or maximum) value, it names one subregion as an example. The
complete list of these regions can be viewed by hovering over the
info icon . The next sentence lists the regions that are univariate
outliers according to the _focus_ variable (text node _Uni. outlier_
_desc._ ). This and all other similar lists of subregions are restricted
to show only 2 to 4 subregions according to the dynamic selection
method (Section 4.3) with the possibility to view the complete list
on demand.

Next, in the second paragraph, the text node _Outlier among_
_neighbors desc._ is responsible for describing the regions that exhibit substantially different values compared to their adjacent
subregions. We use the method described in Section 3.3.1, Tukey’s
fences, for identifying local outliers. It works well if the number of adjacent subregions is larger (e.g., for Missouri, Nevada,
Texas, and Wisconsin). However, in the case of a few neighboring
subregions (e.g., Florida has only two adjacent states), cannot
detect meaningful outliers. For this particular case, even Dixon’s
Q test (Dean and Dixon, 1951)–efficient method for detecting outliers in a small number of observations–failed to identify Florida
as an outlier. Since these situations are harder to identify, we take
a conservative decision and exclude all the subregions that have
less than three neighbors from the analysis.

The last sentence of the second paragraph goes into details of
the regional differences found in the values of both variables (text
node _Reg. differences desc._ ). Depending on the regional classification of the geographical region under consideration, we describe



the subregional groups that show distinct behavior compared
to the other groups. For example, Fig. 1 depicts that Southern
states lost more lives to storms in comparison to other states.
The same text node produces another variation of this sentence
in Fig. 6 describing that, although countries in Western Europe
spend more on health, Southern European countries have higher
average life expectancies.

The final paragraph highlights the relationship of the _context_
to the _focus_ variable followed by a description of bivariate outliers. It begins by describing a positive or negative correlation
among the variables (text node _Pos./neg. correlation_ ). In the case of
_Causality_ set to _yes_, a different phrasing and vocabulary is used to
imply causality. For instance, Fig. 1, third paragraph, it is stated
that _‘‘Texas experienced a high number of deaths as a result of a_
_high number of storms’’_ . The choice of the phrase _‘‘as a result of"_ is
specific to causality. The first sentence of this paragraph is not
available in Fig. 1 as the overall value of correlation is below
the threshold value (shown in Fig. 5); Fig. 6 gives an example
of this sentence. The presence of a strong positive or negative
correlation among one or more subregional groups is highlighted
in the next sentence (text node _Reg. corr. desc._ ). Then follows the
description of regions that show bivariate outliers. For instance,
Fig. 1 highlights that the states of Texas and Nevada are bivariate outliers—Texas having maximum values for both variables
whereas Nevada suffered a very high number of casualties in a
relatively small number of storms.


_5.3. On-demand explanations_


The _overview_ section provides a high-level summary of the
analysis and does not include descriptions of every subregion.
Therefore, in addition to the tool-tips showing the values of the
_focus_ and _context_ variables, we present additional descriptions
on every subregion. Users can click any subregion to acquire
additional details that are displayed below the _overview_ section
as shown in Fig. 1. The generation process for the on-demand
explanations follows a similar decision graph to the one shown
in Fig. 5; the generated text consists of a single paragraph.


34 _S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_


**Table 2**
Parameter configuration for shown examples.


Fig. Title Region Subregion Level Focus Type Context Type Focus Name Context Name Situation Causality


1 _Fatalities caused by_ _USA_ _states_ _casualties_ _incidents_ _deaths_ _storms_ _negative_ _yes_
_storms, USA, 2017_



6 _Average life expectancy_
_and spendings on health,_
_Europe, 2018_


7 _Adolescent birth rates and_
_use of Internet, World,_
_2015_



_Europe_ _countries_ _demographic-_ _monetary_ _average life_ _health expenditure_ _positive_ _no_
_indicators_ _expectancy_


_World_ _countries_ _demographic-_ _percentage_ _adolescent birth_ _Internet users_ _neutral_ _no_
_indicators_ _rate_



8 _Obesity and consumption_ _World_ _countries_ _percentage_ _indicator_ _obese people_ _alcohol consumption_ _negative_ _no_
_of alcohol, World, 2010_



The first sentence compares the values of the _focus_ and _context_
variables for the selected subregion with the respective average
values across all subregions. If the selected subregion is among
one of the extreme cases, it is stated by using quantifiers such as
_highest_, _lowest_, _most_, etc. For instance, in case of Texas, this sentence reads: _‘‘Texas experienced the highest number of deaths (184)_
_and highest number of storms (3621) among all states of the United_
_States of America’’._ The next sentence states the statistical ranking
of the selected subregion with respect to the _focus_ variable. The
last sentence provides a comparison of the selected subregion
with its neighboring regions for highlighting similar or dissimilar
statistics. For instance, the state of Utah is the only state among
its neighboring states that does not report any casualties.

Besides the explanations on one subregion, it is also possible to compare any two subregions by simultaneously selecting
them. Here, the generated text consists of a single sentence that
contrasts both regions based on the values of both variables.
For instance, Figs. 7 and 8 present two different instances of
comparison texts.


**6. Results**


We present a number of examples to demonstrate the usefulness of our approach and support our claims that the _iMR_
(i) detects outliers, regional differences, and prominent patterns
reliably for various datasets, (ii) produces meaningful textual descriptions about the analysis results, and (iii) adapts to different
variable types and different levels of subregional granularity. In
addition to the examples presented in this section, readers can
explore more examples by running the _iMR_ system in any modern
Web browser.

In what follows, we demonstrate map reports for three different _Regions_ : world (Figs. 7 and 8), continent (Fig. 6), and
country (Fig. 1) and two different _Subregional Levels_ : countries
and states. Table 2 shows the values of the user-defined parameters for the examples. At _world_ level, the report describes the
group of countries showing distinct behavior. For instance, the
European countries have higher numbers of Internet users and
lower adolescent birth rates in comparison to the rest of the
world. On the continent level, Fig. 6 reports the differences among
various parts of Europe—countries in Southern Europe have better
average life expectancies despite spending less on health. At the
country level, in addition to describing the differences across
various states of the country, the report also highlights the states
showing dissimilar behavior in contrast to their adjacent states.
For instance, Fig. 1 shows that the states Missouri, Nevada, and
Wisconsin suffered a lot more deaths than their neighbors.

To show the adaptability of the generated text to various
situations, we showcase examples for each type of _situation_ . Fig. 7
highlights the relationship between adolescent birth rates—the
annual number of live births per women aged 15–19, and the
number of people who have access to the Internet. The adolescent



birth rate ( _focus_ ) is neither clearly positive nor negative, this
report is generated according to the _neutral_ situation.

The map reports shown in Figs. 1 and 8 are produced with the
_negative_ value of the _Situation_ . For instance, the phrase _‘‘suffered_
_a lot more casualties"_ (Fig. 1). Although both examples share the
same value of the _situation_, the narrative differs considerably
based on the variable types and the presence of correlations. The
former example highlights the presence of a positive correlation
among Southern states while there was not considerable correlation for the entire USA. In contrast, there is no paragraph about
correlations between variables in Fig. 8 as the value is not large
enough.

Fig. 6 presents the average life expectancy and the money per
household spent on health. Here, higher values of life expectancy
are favorable so the _situation_ is _positive_ . The phrase _‘‘better is the_
_life expectancy"_, reflects the positive character of the situation
while describing the higher values of the _focus_ variable.

Mostly, the choice of quantifiers and verbs depends on the
variable type. For instance, Fig. 1 uses the _casualties_ as the type
of the _focus_ variable and hence the phrase _‘‘number of"_ is used.
Similar is the case with variable type _percentage_ in Fig. 7 ( _‘‘per-_
_centage of Internet users’’_ ) and Fig. 8 ( _‘‘percentage of obese people’’_ ).
Referring to Fig. 6, the choice of quantifier _‘‘values of"_ for the
variable _health expenditure_ is based on the variable type _monetary_ .
However, the variable type _demographic-indicators_ does not need
any phrase as seen in the examples of Fig. 6 and Fig. 7 ( _‘‘African_
_countries showed higher adolescent birth rates’’_ ). In Fig. 1, the verbs
_‘‘suffered"_, _‘‘experienced"_, and _‘‘faced"_ correspond to _Focus Type_ ←
_casualties_ .


**7. Discussion and conclusion**


We demonstrated an approach to create bivariate geostatistical data analysis reports consisting of generated narrative
accompanying a map visualization. The reports guide through the
analysis results and provide additional explanations for interpreting the data. Through a number of examples, we have shown the
flexibility of our approach and that it produces meaningful interactive reports for different variable types, geographic regions, and
scenarios.

The scope of our work is limited to bivariate geo-statistical
(i.e., numeric) data where one variable potentially influences
the other. While we chose a specific geographic visualization to
encode the bivariate data, it would be relatively easy to replace
the visualization by a different one or even make it customizable.
An option to achieve it could be the use of a comprehensive
declarative model for producing visualizations as described by Jo
et al. (2019). We have coverage for a number of variable types,
but cannot claim that every variable can be classified as one of the
mentioned categories. However, the generic category _quantitative_
results in a less tailored but still meaningful narrative. Interesting future work includes extending the approach to categorical
variables, multivariate data (i.e., more than two variables), and


_S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_ 35


**Fig. 7.** An interactive map report showing the possible relationship between adolescent birth rates and the percentage of Internet users across countries of the world
in 2015.


**Fig. 8.** An interactive map report describing the percentage of obese people and alcohol consumption in the world during 2010.


36 _S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_



spatiotemporal information. While the first extension is estimated to require only smaller changes, the two latter scenarios
will likely require substantially different data analysis, narration,
and visualization techniques. In contrast to most previous systems that generate combined visual and textual descriptions, our
focus is comparatively broad and covers different scenarios. The
use of a small set of parameters gives sufficient flexibility to
tailor the same text generation process for different datasets.
Hence, our approach can be considered as lying between the
fully automated text generation systems (which are tailored to a
narrow scenario) and tools that allow for building fully customizable templates. However, our approach does not support manual
refining or extending the reports beyond the configurations that
can be specified through the parameters.

Since our map reports contain text and visualizations, as two
different parts of the report, one might argue that this introduces a split-attention effect. However, this is true for any representation of data that includes multiple views. The available
interactions in our reports counterbalance this effect by providing an easier and quicker way of cross-referencing the two
representations. Furthermore, the use of word-sized graphics also
helps better integrating textual and visual information (Beck and
Weiskopf, 2017).

One problem with the auto-generated reports like ours is that
the possibility of incorrect information being generated cannot
be excluded. One might argue that the said problem endangers
visualizations to some extent as well especially when the mapping between data and visual elements is complex. However,
the problem is more severe with auto-generated text as it is
more explicit. Like for any complex software system, one possible
countermeasure is to apply thorough testing.

At the moment our reports are generated based on pre-defined
settings and do not take into account user interactions in the
generation process. It would be interesting to consider exploration histories, and even relative user characteristics (as found
in Toker et al.’s work (Toker et al., 2018)). In addition to the ondemand textual explanations, the use of summary visualizations
as discussed by Monmonier (1990) to reveal relationships among
variables on a sub-selection of regions can further enrich the
documents.

Although it is obvious that both visual and textual data descriptions have their advantages, it remains a largely open research question which information is better represented in which
modality. Some existing works have already provided evidence
that a bimodal (i.e., text and visualization) representation can
be beneficial for understanding and interpreting the information. Gkatzia et al. (2017) demonstrate better decision making
under uncertainty using a task-based study. Similarly, Sripada
and Gao (2007) claim that divers find the bimodal representation more comprehensive while judging the safety of a deep
dive. However, their results are based on specific datasets and
cannot be generalized. Our approach assumes that a bivariate
map visualization is given; the narration only accompanies the
visual representation, but is not considered to live without the
visualization. As a next step, it would be interesting to perform
user studies to investigate if especially users rather inexperienced
with visualization will profit from the additional text as expected.


**Acknowledgment**


Fabian Beck is indebted to the Baden-Württemberg Stiftung
for the financial support of this research project within the Postdoctoral Fellowship for Leading Early Career Researchers.


**Appendix A. Supplementary data**


Supplementary material related to this article can be found
[online at https://doi.org/10.1016/j.visinf.2019.03.004.](https://doi.org/10.1016/j.visinf.2019.03.004)



**References**


Beck, F., Siddiqui, H.A., Bergel, A., Weiskopf, D., 2017. Method execution reports:

Generating text and visualization to describe program behavior. In: Proceedings of the 5th IEEE Working Conference on Software Visualization. IEEE, pp.
[1–10. http://dx.doi.org/10.1109/VISSOFT.2017.11.](http://dx.doi.org/10.1109/VISSOFT.2017.11)
Beck, F., Weiskopf, D., 2017. Word-sized graphics for scientific texts. IEEE Trans.

[Vis. Comput. Graphics 23 (6), 1576–1587. http://dx.doi.org/10.1109/TVCG.](http://dx.doi.org/10.1109/TVCG.2017.2674958)
[2017.2674958.](http://dx.doi.org/10.1109/TVCG.2017.2674958)

Braun, D., Reiter, E., Siddharthan, A., 2018. Saferdrive: An NLG-based behaviour

[change support system for drivers. Nat. Lang. Eng. 1–38. http://dx.doi.org/](http://dx.doi.org/10.1017/S1351324918000050)
[10.1017/S1351324918000050.](http://dx.doi.org/10.1017/S1351324918000050)
Brewer, C., Campbell, A.J., 1998. Beyond graduated circles: varied point symbols

for representing quantitative data on maps. Cartogr. Perspect. (29), 6–25.
[http://dx.doi.org/10.14714/CP29.672.](http://dx.doi.org/10.14714/CP29.672)
Brewer, C.A., MacEachren, A.M., Pickle, L.W., Herrmann, D., 1997. Mapping

mortality: Evaluating color schemes for choropleth maps. Ann. Assoc. Am.
[Geogr. 87 (3), 411–438. http://dx.doi.org/10.1111/1467-8306.00061.](http://dx.doi.org/10.1111/1467-8306.00061)
[Dale, R., Geldof, S., Prost, J.-P., 2005. Using natural language generation in](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb6)

[automatic route description. J. Res. Pract. Inf. Technol. 37 (1), 89.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb6)
Dean, R.B., Dixon, W., 1951. Simplified statistics for small numbers of
observations. Anal. Chem. 23 (4), 636–638. [http://dx.doi.org/10.1021/](http://dx.doi.org/10.1021/ac60052a025)
[ac60052a025.](http://dx.doi.org/10.1021/ac60052a025)
Deemter, K.V., Theune, M., Krahmer, E., 2005. Real versus template-based natural

language generation: A false opposition? Comput. Linguist. 31 (1), 15–24.
[http://dx.doi.org/10.1162/0891201053630291.](http://dx.doi.org/10.1162/0891201053630291)
Demir, S., Carberry, S., McCoy, K.F., 2012. Summarizing information graphics

[textually. Comput. Linguist. 38 (3), 527–574. http://dx.doi.org/10.1162/COLI_](http://dx.doi.org/10.1162/COLI_a_00091)
[a_00091.](http://dx.doi.org/10.1162/COLI_a_00091)
[Elmer, M.E., 2012. Symbol Considerations for Bivariate Thematic Mapping (Ph.D](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb10)

[thesis), University of Wisconsin–Madison.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb10)
Flannery, J.J., 1971. The relative effectiveness of some common graduated point

symbols in the presentation of quantitative data. Cartographica 8 (2), 96–109.
[http://dx.doi.org/10.3138/J647-1776-745H-3667.](http://dx.doi.org/10.3138/J647-1776-745H-3667)
Gatt, A., Krahmer, E., 2018. Survey of the state of the art in natural language

generation: Core tasks, applications and evaluation. J. Artificial Intelligence
[Res. 61, 65–170. http://dx.doi.org/10.1613/jair.5477.](http://dx.doi.org/10.1613/jair.5477)
Gkatzia, D., Lemon, O., Rieser, V., 2017. Data-to-text generation improves

decision-making under uncertainty. IEEE Comput. Intell. Mag. 12 (3), 10–17.
[http://dx.doi.org/10.1109/MCI.2017.2708998.](http://dx.doi.org/10.1109/MCI.2017.2708998)
Goffin, P., Willett, W., Fekete, J.-D., Isenberg, P., 2014. Exploring the placement

and design of word-scale visualizations. IEEE Trans. Vis. Comput. Graphics
[20 (12), 2291–2300. http://dx.doi.org/10.1109/TVCG.2014.2346435.](http://dx.doi.org/10.1109/TVCG.2014.2346435)
[Härdle, W., Simar, L., 2007. Applied Multivariate Statistical Analysis, vol. 22007.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb15)

[Springer.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb15)
[Hoaglin, D.C., Mosteller, F., Tukey, J.W., 2000. Understanding Robust and](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb16)

[Exploratory Data Analysis, vol. 1. Wiley Classic Library.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb16)
Howard, D., MacEachren, A.M., 1996. Interface design for geographic visualiza
tion: Tools for representing reliability. Cartogr. Geogr. Inf. Syst. 23 (2), 59–77.
[http://dx.doi.org/10.1559/152304096782562109.](http://dx.doi.org/10.1559/152304096782562109)
Hullman, J., Diakopoulos, N., Adar, E., 2013. Contextifier: automatic generation

of annotated stock visualizations. In: Proceedings of the SIGCHI Conference
[on Human Factors in Computing Systems. CHI, ACM, pp. 2707–2716. http:](http://dx.doi.org/10.1145/2470654.2481374)
[//dx.doi.org/10.1145/2470654.2481374.](http://dx.doi.org/10.1145/2470654.2481374)
Hunter, J., Gatt, A., Portet, F., Reiter, E., Sripada, S., 2008. Using natural language

generation technology to improve information flows in intensive care units.
[In: ECAI, pp. 678–682. http://dx.doi.org/10.3233/978-1-58603-891-5-678.](http://dx.doi.org/10.3233/978-1-58603-891-5-678)
Jain, A., Keller, J.M., 2015. Textual summarization of events leading to health

alerts. In: Engineering in Medicine and Biology Society, 37th Annual Inter[national Conference of the IEEE. EMBC ’15, pp. 7634–7637. http://dx.doi.org/](http://dx.doi.org/10.1109/EMBC.2015.7320160)
[10.1109/EMBC.2015.7320160.](http://dx.doi.org/10.1109/EMBC.2015.7320160)
Jo, J., Vernier, F., Dragicevic, P., Fekete, J.-D., 2019. A declarative rendering

model for multiclass density maps. IEEE Trans. Vis. Comput. Graphics 25
[(1), 470–480. http://dx.doi.org/10.1109/TVCG.2018.2865141.](http://dx.doi.org/10.1109/TVCG.2018.2865141)
Kim, S., Maciejewski, R., Malik, A., Jang, Y., Ebert, D.S., Isenberg, T., 2013. Bristle

maps: A multivariate abstraction technique for geovisualization. IEEE Trans.
[Vis. Comput. Graphics 19 (9), 1438–1454. http://dx.doi.org/10.1109/TVCG.](http://dx.doi.org/10.1109/TVCG.2013.66)
[2013.66.](http://dx.doi.org/10.1109/TVCG.2013.66)
Kwon, B.C., Stoffel, F., Jäckle, D., Lee, B., Keim, D., 2014. VisJockey: En
riching data stories through orchestrated interactive visualization. In:
Computation+Journalism Symposium 2014.
Latif, S., Beck, F., 2019. VIS Author profiles: Interactive descriptions of publication

records combining text and visualization. IEEE Trans. Vis. Comput. Graphics
[25 (1), 152–161. http://dx.doi.org/10.1109/TVCG.2018.2865022.](http://dx.doi.org/10.1109/TVCG.2018.2865022)
[MacEachren, A.M., 2004. How Maps Work: Representation, Visualization, and](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb25)

[Design. Guilford Press.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb25)
[Mittal, V.O., Roth, S.F., Moore, J.D., Mattis, J., Carenini, G., 1995. Generat-](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb26)

[ing explanatory captions for information graphics. In: Proceedings of the](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb26)
[14th International Joint Conference on Artificial Intelligence. IJCAI, Morgan](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb26)
[Kaufmann Publishers Inc., pp. 1276–1283.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb26)


_S. Latif and F. Beck / Visual Informatics 3 (2019) 27–37_ 37



Molina, M., Sanchez-Soriano, J., Corcho, O., 2015. Using open geographic data

to generate natural language descriptions for hydrological sensor networks.
[Sensors 15 (7), 16009–16026. http://dx.doi.org/10.3390/s150716009.](http://dx.doi.org/10.3390/s150716009)
Monmonier, M., 1990. Strategies for the visualization of geographic time-series

[data. Cartographica 27 (1), 30–45. http://dx.doi.org/10.3138/U558-H737-](http://dx.doi.org/10.3138/U558-H737-6577-8U31)
[6577-8U31.](http://dx.doi.org/10.3138/U558-H737-6577-8U31)
Nelson, E., 2000. The impact of bivariate symbol design on task performance in

[a map setting. Cartographica 37 (4), 61–78. http://dx.doi.org/10.3138/V743-](http://dx.doi.org/10.3138/V743-K505-5510-66Q5)
[K505-5510-66Q5.](http://dx.doi.org/10.3138/V743-K505-5510-66Q5)
Ramos-Soto, A., Bugarin, A.J., Barro, S., Taboada, J., 2015. Linguistic descriptions

for automatic generation of textual short-term weather forecasts on real
[prediction data. IEEE Trans. Fuzzy Syst. 23 (1), 44–57. http://dx.doi.org/10.](http://dx.doi.org/10.1109/TFUZZ.2014.2328011)
[1109/TFUZZ.2014.2328011.](http://dx.doi.org/10.1109/TFUZZ.2014.2328011)
Ramos-Soto, A., Vazquez-Barreiros, B., Bugarín, A., Gewerc, A., Barro, S., 2017.

Evaluation of a data-to-text system for verbalizing a learning analytics
[dashboard. Int. J. Intell. Syst. 32 (2), 177–193. http://dx.doi.org/10.1002/int.](http://dx.doi.org/10.1002/int.21835)
[21835.](http://dx.doi.org/10.1002/int.21835)
[Reiter, E., Dale, R., Feng, Z., 2000. Building Natural Language Generation Systems.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb32)

[MIT Press.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb32)
Rousseeuw, P.J., Ruts, I., Tukey, J.W., 1999. The bagplot: A bivariate boxplot.

[Amer. Statist. 53 (4), 382–387. http://dx.doi.org/10.1080/00031305.1999.](http://dx.doi.org/10.1080/00031305.1999.10474494)
[10474494.](http://dx.doi.org/10.1080/00031305.1999.10474494)
Srinivasan, A., Drucker, S.M., Endert, A., Stasko, J., 2019. Augmenting vi
sualizations with interactive data facts to facilitate interpretation and
[communication. IEEE Trans. Vis. Comput. Graphics 25 (1), 672–681. http:](http://dx.doi.org/10.1109/TVCG.2018.2865145)
[//dx.doi.org/10.1109/TVCG.2018.2865145.](http://dx.doi.org/10.1109/TVCG.2018.2865145)



Sripada, S.G., Gao, F., 2007. Summarizing dive computer data: A case study

in integrating textual and graphical presentations of numerical data. In:
Workshop on Multimodal Output Generation. MOG ’07, p. 149.
Thomas, K., Sripada, S., 2007. Atlas.txt: Linking geo-referenced data to text

for NLG. In: Proceedings of the Eleventh European Workshop on Natural
Language Generation. ENLG ’07, pp. 163–166.
Toker, D., Conati, C., Carenini, G., 2018. User-adaptive support for processing

magazine style narrative visualizations: Identifying user characteristics that
matter. In: 23rd International Conference on Intelligent User Interfaces. ACM,
[pp. 199–204. http://dx.doi.org/10.1145/3172944.3173009.](http://dx.doi.org/10.1145/3172944.3173009)
[Tufte, E.R., 2006. Beautiful Evidence, first ed. Graphics Press.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb38)
[Tukey, J.W., 1977. Exploratory Data Analysis, vol. 2. Reading, Mass.](http://refhub.elsevier.com/S2468-502X(19)30019-1/sb39)
Turner, R., Sripada, S., Reiter, E., Davy, I.P., 2008. Using spatial reference frames to

generate grounded textual summaries of georeferenced data. In: Proceedings
of the Fifth International Natural Language Generation Conference. INLG ’08,
Association for Computational Linguistics, Stroudsburg, PA, USA, pp. 16–24.
[http://dx.doi.org/10.3115/1708322.1708328.](http://dx.doi.org/10.3115/1708322.1708328)
United Nations, 1999. Statistical Division, Countries or areas / geographical

[regions. https://unstats.un.org/unsd/methodology/m49.](https://unstats.un.org/unsd/methodology/m49)
Wahlster, W., André, E., Finkler, W., Profitlich, H.J., Rist, T., 1993. Plan-based

integration of natural language and graphics generation. Artificial Intelligence
[63 (1–2), 387–427. http://dx.doi.org/10.1016/0004-3702(93)90022-4.](http://dx.doi.org/10.1016/0004-3702(93)90022-4)


