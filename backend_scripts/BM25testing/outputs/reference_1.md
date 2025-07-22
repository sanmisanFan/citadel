-~ ____


_**Chris Brunsdon,**_ **A.** _**Stewart Fotheringham**_

_**and Martin**_ _**E.**_ _**Charlton**_


_**Geographically Weighted Regression:**_ **A** _**Method**_
_**`for`**_ _**Exploring Spatial Nonstationarity**_


_Spatial nonstationarity is a condition_ _in_ _which a simple ‘global” model cannot_
_explain the relationships between some sets of variables. The nature of the_
_model must alter over space to reflect the structure within the data._ _In_ _this_
_paper, a technique is developed, termed which attempts to capture this variation by Cali_ geogra hically weighted regression, **E** _rating a multiple regression_

_model which allows diferent relationships_ _to_ _exist at diferent points in space._
_This technique is loosely based on kernel regression. The method itself is intro-_
_duced and related issues such as the choice of a spatial weighting function are_
_discussed. Following_ _this,_ _a series of related statistical tests are considered_
_which can be described generally as tests for spatial nonstationarity. Using_
_Monte Carlo methods, techniques are proposed for investigatin_ _the null_

_hypothesis that the data_ _m y_ _be described_ _by_ _a global model rat_ a _er than a_

_non-stationa_ **`y`** _one and also for testing whether individual regression_ _**coefi-**_
_cients are stable over geographic space. These techniques are demonstrated on a_
_data set from the_ _1991_ _**`U.`**_ _**`K.`**_ _census relating car ownership rates to social class_
_and mule unemployment. The paper concludes by discussing ways in which the_
_technique can_ _be_ _extended._


**`1.`** **INTRODUCTION**


One of the main objectives in spatial analysis is to identify the nature of relationships that exist between variables. Typically this is undertaken by calculating
statistics or estimating parameters with observations taken from different spatial
units across a study area. The resulting statistics or parameter estimates are
assumed to be constant across space although this might be a very questionable
assumption to make in many circumstances. It seems reasonable to assume that
there might be intrinsic differences in relationships over space or that there
might be some problem with the specification of the model from which the relationships are being measured and which manifests itself in terms of spatially


_**Dr.**_ _Chris Brunsdon is lecturer in computer-based methods in the Department_ _**`of`**_ _Town_
_and County Planning, A. Stewart Fotheringham_ is _Professor_ _**`of`**_ _Quantitative Geography,_
_and Martin Charlton_ **is** _lecturer_ _in_ _GIS_ _in the Department_ _**`of`**_ _Geography, all_ _at_ _Newcastle_
_University._


_Geographical Analysis,_ **Vol.** **28,** _No._ **4** **(October 1996)** _`0`_ **1996 Ohio State University Press**
**Submitted 6/7/95. Revised version accepted 2/16/96.**


