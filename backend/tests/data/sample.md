1 

## LAMDA: Aiding Visual Exploration of Atomic Displacements in Molecular Dynamics Simulations 

Rostyslav Hnatyshyn, Danny Perez, Gerik Scheuermann, Ross Maciejewski, Baldwin Nsonga 

_**Abstract**_ **—Contemporary materials science research is heavily conducted** _**in silico**_ **, involving massive simulations of the atomicscale evolution of materials. Cataloging basic patterns in the atomic displacements is key to understanding and predicting the evolution of physical properties. However, the combinatorial complexity of the space of possible transitions coupled with the overwhelming amount of data being produced by highthroughput simulations make such an analysis extremely challenging and time-consuming for domain experts. The development of visual analytics systems that facilitate the exploration of simulation data is an active field of research. While these systems excel in identifying temporal regions of interest, they treat each timestep of a simulation as an independent event without considering the behavior of the atomic displacements between timesteps. We address this gap by introducing LAMDA, a visual analytics system that allows domain experts to quickly and systematically explore state-to-state transitions. In LAMDA, transitions are hierarchically categorized, providing a basis for cataloging displacement behavior, as well as enabling the analysis of simulations at different resolutions, ranging from very broad qualitative classes of transitions to very narrow definitions of unit processes. LAMDA supports navigating the hierarchy of transitions, enabling scientists to visualize the commonalities between different transitions in each class in terms of invariant features characterizing local atomic environments, and LAMDA simplifies the analysis by capturing user inputs through annotations. We evaluate our system through a case study and report on findings from our domain experts.** 

_**Index Terms**_ **—Molecular dynamics, Visual analytics** 

## I. INTRODUCTION 

OLECULAR dynamics (MD) simulations are a pow- **M** erful tool in the computational sciences, including materials science, physics, chemistry, and biology. They provide a fully spatio-temporally resolved view of the nanoscale behavior of materials in terms of the displacements of individual atoms, which otherwise are extremely difficult to observe experimentally. The information extracted from these simulations can be used to elucidate basic unit-steps in the evolution of materials, calibrate larger-scale models, or even directly predict the outcome of experiments. 

MD simulations correspond to the solution of a large set of ordinary differential equations (the classical atomistic equations of motion) that describe the evolution of the positions and velocities of atoms in a material. The solution of these 

R. Hnatyshyn and R. Maciejewski are with Arizona State University, USA. E-mail: _{_ rhnatysh,rmacieje _}_ @asu.edu. 

D. Perez is with Los Alamos National Laboratory, USA. E-mail: _{_ danny perez _}_ @lanl.gov 

G. Scheuermann and B. Nsonga are with Leipzig University, Germany. E-mail: _{_ scheuermann, nsonga _}_ @informatik.uni-leipzig.de. 

equations requires an approximation of the interaction energy between atoms, from which the interatomic forces can be obtained and the equations integrated using a simple explicit numerical scheme. These simulations generate immense volumes of data, as a single MD trajectory can be thought of as a point evolving in 3 _N_ atoms dimensions (or even 6 _N_ atoms when including velocities) over millions of timesteps (a typical timestep being a _femtosecond_ , i.e., 10 _[−]_[15] seconds). This makes the storage, processing, and visualization of MD trajectories a challenging endeavor. 

In many systems of interest, the energy landscape that characterizes atomic interactions contains relatively deep wells that temporarily confine the motion of atoms. This makes atomic motion, to a first approximation, a discrete process where long periods of uneventful vibrations are interrupted by infrequent-but-rapid transitions between different wells of the energy landscape. The dynamics of a system are further simplified by representing the energy well through a single configuration, often that of the minimum energy configuration within the well [1]. This compresses an entire continuous highdimensional MD trajectory into a much sparser representation in terms of a discrete _state-to-state trajectory_ between atomic configurations. In spite of this significant simplification, understanding, cataloging, and classifying these transitions is a formidable challenge, given the combinatorial complexity of describing the collective motion of atoms in complex systems. This task is extremely important, as changes to the structure of a system can affect its physical and chemical properties. For instance, the shape of metallic nanoparticles directly influences their catalytic properties [2]. Investigating atomic displacements can reveal exactly _how_ these changes occur. As such, the development of systematic methods and tools for the exploration and categorization of atomic transitions is a pressing need in the applied computational science community. 

While powerful tools are available to investigate and characterize individual _states_ (also referred to as _snapshots_ ) [3]–[7], the ecosystem of tools available to investigate the displacement of atoms between states, referred to as _transitions_ , is comparatively much less developed. Instead, researchers examine transitions one-by-one, using tools such as OVITO [8]. Based on their findings, analysts then classify these transitions into groups. Such a process is prohibitively slow for large datasets, limiting the insights that can be obtained. To our knowledge, there is no tool available to efficiently navigate, compare, and classify ensembles of transitions. 

To address this gap, we present a visual analytics system called **LAMDA** , a recursive acronym that stands for **LAMDA** 

10.1109/TVCG.2026.3652905 © 2026 IEEE 

2 

**Aids Molecular Displacement Analysis** . LAMDA organizes transition ensembles through a series of guided data preprocessing steps: a session starts with the interactive reduction of an input dataset, which lessens the cognitive burden on the analyst without giving up valuable information. Afterwards, the reduced transition ensemble is organized using a hierarchical clustering approach. The results of the clustering can be explored in detail through a suite of multiple coordinated views, ranging from abstract overviews to fully interactive 3D visualizations. To further assist exploration, LAMDA supports comparisons between clusters of transitions through a novel aggregate 3D representation. Insights gained during an analysis can be retained through the system’s note-taking features. To evaluate LAMDA’s efficacy, we present a case study in which we analyze a large ensemble of transitions alongside our domain expert collaborator. This work contributes the following: 

- The application of tensor visualization approaches to encode transitions; 

- A view that supports the exploration of hundreds of transitions with fully interactive 3D visualizations coupled with _insight provenance_ [9] interactions; 

- A visual analytics system that combines these designs with informative overviews and interactions to support analysts in exploring a transition ensemble. 

## II. RELATED WORK 

In this section, we review various methods to analyze long-duration molecular dynamics simulations and discuss the visualization techniques and tools that inspired our system. 

## _A. Quantitative Methods_ 

Atomic configurations of materials are often characterized through the analysis of the spatial relationships between atoms and their neighbors, e.g., the Common Neighbor Analysis [10] and the Ackland-Jones Analysis [11]. These analyses characterize local atomic environments in terms of scalar functions that capture structural characteristics such as local symmetry, enabling the automatic determination of local crystal structure and other basic crystallographic quantities which are commonly used by materials scientists. Although designed to characterize static structures, these features can also be adapted to characterize transitions by examining how they change across the progression from an initial to a final state, a strategy LAMDA automatically applies to input data during the pre-processing stage (cf. subsection V-A). 

The offering of features available to characterize local atomic environments has dramatically increased following the development of modern machine learning techniques to estimate the energy functional used to drive MD simulations. Under this approach, the energetic contribution of each atom in the system is approximated as a learnable function of per-atom features that describe the local atomic arrangement in their neighborhood [12]–[14]. These features typically obey the same translation/rotation/permutation invariance as the energy of the system, as the absolute pose of a system in space should not affect the classification of states and transitions. 

## _B. Visualizing Molecular Dynamics Trajectories_ 

Kocincov´a et al. [15] introduced a visual analytics system that allows for the comparison of secondary protein structures without the typical occlusion issues presented by 3D visualizations by introducing an abstraction that converts two structures into a sequential representation. While this abstraction is powerful and informative, it does not provide information on atomic displacements but rather highlights differences between protein chains; moreover, it is designed for biological molecular systems, which is not the focus of our work. Mehta et al. [16] proposed several techniques that use the 3D locations of atoms as well as the electron density data produced by quantum calculations to evaluate salient isovalues used for isosurface extraction and rendering. Unfortunately, these techniques are limited to analyzing anomalous structures in single atomic configurations and do not consider atomic displacements; moreover, quantum calculations are computationally expensive, especially for long-duration simulations. TRAJELIX [17] derives scalar values from the differences between a reference helical structure and a MD state and displays these transformations as time-series plots, providing an overview of the transformations that occurred during a simulation. These techniques are limited to the analysis of molecules that have a helical structure (i.e., proteins, ligands, etc.). VIA-MD [18] highlights regions of interest in biochemical molecular dynamics trajectories using a combination of 2D and 3D linked views. Our approach focuses on much smaller systems than the ones explored by VIA-MD which experience major structural changes throughout the trajectory. OVITO [19] is widely used among domain experts to visualize single configurations and offers a variety of domain-specific analyses that provide an enormous amount of information; it is the tool of choice for our collaborators. However, OVITO visualizations are designed to only show one configuration at a time. Analyzing a _transition_ entails switching the visualization between its initial and final states without any continuity provided, making it a task teeming with potential cognitive overload. To the best of our knowledge, no extant systems are designed to extract insights from the temporal relations of atomic configurations. 

## _C. Visual Cluster Analytics_ 

LAMDA takes advantage of hierarchical clustering algorithms to form groups of related transitions for the analyst to explore. In this section, we review various visual analytics systems that facilitate cluster exploration. 

DICON [20] generates icons that act as overviews for clusters of high-dimensional data based on the values of its individual members. These overviews not only present the cluster’s content at a glance but also help viewers evaluate the quality of a cluster. Our overview of transition clusters, the _Group Displacement_ visualization, is partially inspired by this approach, as we discovered during our design process that experts find cluster quality information highly valuable during an analysis. VICTOR [21] is a hierarchical clustering visual analytics system that facilitates cluster comparison through the use of various statistical graphics. VICTOR supports variety of 

3 

different visualizations that provide alternative perspectives on the results of a clustering, and the paper as a whole serves as a valuable design study for developing cluster analytics applications. ClusterSculptor [22] is a general-purpose cluster editing system with coordinated views that support both the analysis and modification of the results of a clustering algorithm. Our decision to link the hierarchical heatmap with the dendrograms was inspired by their approach. Thygesen et al. [23] explored a similar scheme for exploring photochemical transition ensembles using the results of a hierarchical clustering algorithm. We note that this paper presents a pipeline and not a fully integrated visual analytics system. Besides this, we focus on the _structural_ changes between nanoparticle states, while this approach focuses on the _electronic_ changes in states. 

## III. ANALYTICAL TASKS AND REQUIREMENTS 

LAMDA builds upon our previous work, MolSieve [3], a visual analytics system that helps analysts discover temporal regions in MD simulations containing significant structural changes, referred to as _transition regions_ . 

We discovered that while MolSieve was useful for identifying transition regions, examining and classifying state-to-state transitions was difficult, as MolSieve is designed with singlestate analysis in mind. Our collaborators would export regions of interest and then manually examine them as ensembles of transitions with external tools. While this task was not nearly as laborious as combing through entire simulations, transition regions can still contain thousands of unique and highly complex transitions, posing a significant barrier to their interpretation. In this section, we discuss our motivations for building LAMDA in terms of tasks and requirements. 

## _A. Analytical Tasks_ 

To address this issue, we met bi-weekly for two years to develop LAMDA. We adopted an iterative design process during development, working closely with our collaborator, a computational materials scientist with over twenty years of experience. Throughout the design process, we identified a set of analytical tasks that reflect the daily workflow of an expert exploring transition ensembles. 

_**T1: Identify broad groups of transitions.**_ Since molecular dynamics trajectories can be composed of tens of thousands of transitions [24]–[26], our collaborators are interested in categorizing transitions into broad and interpretable classes. Having a robust categorization of a system’s behavior will enable researchers to predict how it will perform under various conditions, provide a means for comparison, and offer an efficient approach to develop simplified models. 

To accomplish this, our collaborators are taking advantage of recent advances in machine learning to cluster transitions. Unfortunately, a set of mathematical descriptors (i.e., features) that can accurately partition ensembles of transitions has not yet been identified. Thus, our collaborators spend a significant portion of their time writing code to generate clusters of transitions and then examining them using classic visualizations such as heatmaps and dendrograms. 

_**T2: Identify what characterizes groups of transitions.**_ If an analyst decides to examine a potential clustering further based on the information they gathered from high-level visualizations, they resort to using 3D renders to qualitatively describe transitions one-by-one before organizing them into subjective groups based on shared physical characteristics. This tends to be a tedious and error-prone process due to the cognitive load presented by reasoning across hundreds of transitions, further compounded by the fact that each transition can consist of tens to hundreds of atoms being displaced, with each transition potentially being oriented on different axes. 

_**T3: Evaluate clustering quality.**_ Analysts need to verify the robustness of the overall clustering, ensuring that it captures the underlying behavior of the system. Verifying the robustness of a clustering method for transitions is difficult because descriptive statistics do not capture the nuances of atomic displacements, while manual comparison is again impractical due to its overwhelming cognitive burden. 

## _B. Requirements_ 

Based on these analytical tasks and their challenges, we derived a set of requirements for a visual analytics system that would streamline the process of generating and examining a new clustering of transitions. 

_**R1: Generate and interactively explore groups of transitions.**_ Analysts should be able to directly provide transition data and a set of features as input; the features should reflect some physical component of each transition as they will be used for clustering. The clustering should be straightforward to explore yet allow for detailed exploration on demand (i.e., down to individual transitions) and should guide analysts towards particularly interesting groups. Visualizations of individual transitions should be able to be customized and rendered with external data for analysis. 

_**R2: Provide an overview for a given group of transitions.**_ Analysts should have a concise overview available for any transition group of interest. This overview should not obscure or abstract spatial information and present the salient theme of the group being explored. It should also simplify the process of comparing groups of transitions. 

_**R3: Provide a means to evaluate cluster quality.**_ Since groups of transitions are identified via machine learning methods, they may include a number of dissimilar transitions. This could indicate that the clustering should be adjusted, so the system should provide a means to quickly identify when clusters are not uniform. 

_**R4: Provide an organized way to store insights gained during exploration.**_ Analysts should be able to store their insights, similar to an ordinary notebook. The notebook-like approach should integrate with the system and guide experts back towards where they discovered their objects of interest. 

_**R5: Export results for further analysis.**_ Analysts should be able to export the insights they gained during the analysis, along with any arbitrary set of transitions. All exported data should be stored in a portable format to facilitate further exploration and scientific discourse. 

4 

_**R6: Visual and computational scalability.**_ The system should reduce the cognitive load on the expert while remaining highly responsive, even when faced with large datasets (several thousand transitions). To support this, redundant transitions should be removed automatically, with the ability to adjust the level of reduction. 

## IV. BACKGROUND 

In this section, we discuss data transformation techniques from the literature that inform our approach. To begin, we define an atomic state (i.e., configuration; snapshot) with _n_ atoms as an _n ×_ 3 matrix _S_ , with the _i[th]_ row corresponding to the 3D coordinates of the _i[th]_ atom. As such, we can view a molecular dynamics simulation as a temporal sequence of _n×_ 3 matrices _M_ = ( _St ,..., SL_ ); _L_ being the length of the sequence and _t_ the timestep of a state. A transition _T_ between two states _S_ 0 and _S_ 1 is then defined as a tuple _T_ = ( _S_ 0 _, S_ 1). The set of transitions described by a simulation is _Tall_ = _{Tt ,..., TL−_ 1 _}_ where _Tt_ is a tuple composed of temporally adjacent states _St_ and _St_ +1 from _M_ . The _i[th]_ row in both matrices must correspond to the same atom; i.e., the states must be consistently labeled. Finally, a _transition ensemble_ is any subset of _Tall_ . 

## _A. Aligning Atomic Displacements_ 

As mentioned previously, we are concerned with the analysis of transitions in a MD simulation, i.e., the motion of the atoms from one state to another. Visually comparing multiple transitions is difficult because they can be oriented arbitrarily. To address this, LAMDA uses alignment techniques to orient transitions as consistently as possible before visualizing them. To the best of our knowledge, the alignment of transitions between atomic configurations has not been explored. 

LAMDA’s alignment approach (Figure 1) is composed of simultaneously computing pose and correspondence registrations, as the optimal mapping of the motions in two different transitions is _a priori_ unknown. To achieve this, we first compute a matrix of _n × k_ per-atom features _f_ for each _state_ , where the _i[th]_ row corresponds to the feature vector for atom _i_ . Then, we calculate ∆ _f_ = _fs_ 1 _− fs_ 2, the difference between the feature matrices of the initial and final states of transition _T_ . Note that these features do not necessarily have to be real physical quantities of an atomistic system; they only need to capture the local structure surrounding the atoms. Consequently, ∆ _f_ is non-zero only for atoms whose local environments are affected by the transition. Natural choices for _f_ are per-atom features used to train machine-learningbased interatomic potentials, as these are specifically designed to capture physically relevant atomic distortions. For instance, we used the Spectral Neighbor Analysis Potentials [27] as _f_ for our case study (c.f. section VI) because they characterize the local atomic environment and are invariant to rotations, translations and permutations. 

With the features prepared, we define two sets of _k pseudoatoms_ for each transition, each set corresponding to one state. The pseudo-atom positions _q j_ (1 _≤ j ≤ k_ ) are permutationinvariant versions of the atomic positions _S_ . These can be 

**==> picture [185 x 137] intentionally omitted <==**

**----- Start of picture text -----**<br>
T' T<br>Ses Gyte:| |e:<br>art ae ats<br>We ne| Ves N<br>q'1 q2 (aligned) q2<br>R < SO(3)<br>€ §=k,<br>T (aligned)<br>EN Arese Aae‘f. he Apply rotation R<br>**----- End of picture text -----**<br>


Fig. 1. Our alignment scheme: the transition _T[′]_ (blue) is being aligned to _T_ (orange). Both transitions contain an initial and final state, where atoms are colored by their changes in bond length. These changes indicate the areas that should be aligned. Pseudo positions ( _qi_ ) are calculated based on a transition’s ∆ _f_ matrix. A point set alignment algorithm is then used to calculate a rotation matrix _R_ that results in an appropriate correspondence indicated by the dotted lines. The matrix _R_ is then applied to _T[′]_ . 

defined in terms of pseudo-center-of-mass position with ∆ _f_ playing the role of effective masses. Formally, 

**==> picture [169 x 25] intentionally omitted <==**

where _α_ indexes cartesian directions. These values can be interpreted as a normalized sum of atom positions, weighted by the rate of change – this approximates a “center of change” for each feature. The positions are independent of the ordering of the atoms within each transition, which allows us to focus on aligning atoms that _change similarly_ rather than relying on their labels for information. The goal of the alignment is to find a pose which aligns these pseudo-atoms so that the displacement patterns of different transitions can easily be compared. 

These pseudo-atoms are then centered so their average position is located at the origin, i.e., 

**==> picture [173 x 25] intentionally omitted <==**

To calculate a possible alignment between two transitions _T[′]_ and _T_ , we use Kabsch’s algorithm [28] to rotationally align their corresponding **ˆq** ’s. If a comparison of transitions that is invariant to the exchange of the initial and final states is preferred, the alignment procedure presented above can be carried out a second time after exchanging initial and final states in _T[′]_ . The ordering that minimizes the residual of the alignment is then selected. We apply this process to align any group _G_ of transitions by arbitrarily selecting a reference transition _Tref_ and aligning all remaining _G_ ’s members to _Tref_ . 

## _B. Finite Strain Theory_ 

We also investigated visualization schemes that encode the relative displacement occurring during a transition from a continuum mechanical perspective using a method introduced by Gullett et al. [29]. This consists of computing the Lagrangian strain tensor _E ∈_ R[3] _[×]_[3] for all atoms in a transition, where 

5 

**==> picture [130 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
S0 interpolated S1<br>K1 K2 K3<br>**----- End of picture text -----**<br>


Fig. 2. An example of the superquadric visualization; it displays the local displacement around each atom without the need for animations. The top row of figures illustrates a typical atomic visualization of a transition, while the bottom row is the same transition visualized as a superquadric, colored with different strain invariants (subsection IV-B). _K_ 1 is the default value used for coloring superquadrics; the others are included for illustrative purposes as they contain higher-order information about the deformation. 

_Ei_ encodes the deformation of the neighborhood of atom _i_ without rotation with reference to its initial state. We associate the resulting tensors with the initial positions of the transition and calculate scalar values that remain invariant [30] under rigid rotations, referred to as _K_ 1 _,_ 2 _,_ 3: 

**==> picture [208 x 63] intentionally omitted <==**

where _E_ ˜ denotes the deviator of _E_ and _λ_ 1, _λ_ 2, and _λ_ 3 denote the eigenvalues of _E_ . While there are a number of different invariants for three-dimensional second-order tensors [31], we found these particular invariants to be well-suited for visualization, as they encode easily interpretable physical properties of transitions. 

These values are used to generate superquadric [30], [32] visualizations of atomic states (Figure 2). _K_ 1 encodes the volume change (dilation) in the neighborhood of the atom. _K_ 2 encodes the magnitude of the distortion in an atom’s neighborhood; when _K_ 2 = 0 (i.e. no distortion), atoms are rendered as regular spheres, indicating isotropic behavior. Since _K_ 2 simply quantifies the amount of distortion, we look to _K_ 3 to get more information on the nature of the distortion when _K_ 2 _>_ 0. _K_ 3 is the so-called mode of distortion satisfying _−_ 1 _≤ K_ 3 _≤_ 1. The spheres continuously morph into a rodshaped glyph for _K_ 3 = _−_ 1 (linear anisotropy) or a diskshaped glyph for _K_ 3 = +1 (planar anisotropy). All three of these invariants are used to calculate the shape of each glyph (subsection V-B.b), while only _K_ 1 is used for coloring them. 

## V. LAMDA 

LAMDA’s workflow (Figure 3) guides experts through an interactive reduction and clustering process before letting them explore the dataset. Analysis is supported at any level of detail, which can range from the abstract perspectives provided by heatmaps and dendrograms ( **T1** ) to detailed 3D visualizations 

of individual transitions ( **T2** ). Notably, LAMDA provides a suite of interactive visualizations that act as an overview of atomic behavior within a group and provide visual indicators of the quality of a cluster (subsection V-B.c; **T3** ). LAMDA also includes a set of help tooltips for views with special interactions to facilitate on-boarding [33] with the system. These tooltips include information on hotkeys, possible interactions, as well as the interpretation of certain visualizations, e.g., superquadrics (subsection V-B.b). 

LAMDA uses interactive visual linking throughout its interface to mitigate issues with cognitive strain caused by contextswitching. All visual representations of both transitions and clusters are linked to all of their other instances throughout the system. To further mitigate cognitive strain and reduce visual distances for comparisons, we included a view for _insight provenance_ in the _Selection Window_ called the _Scratchpad_ (subsection V-F), where practitioners can freely position embedded 3D visualizations of transitions and clusters to track their analytical process. LAMDA is implemented using the Julia programming language and the Makie [34] graphics framework as a desktop application, with some of the data pre-processing operations (subsection V-A) being powered by the Atomistic Simulation Environment (ASE) library [35]. The color scales used for most visualizations were selected from the set of perceptually uniform scales introduced by Kovesi [36]; the heatmaps throughout the interface use the _linear worb_ scale, while the dendrograms use the dynamic color scheme introduced by Tennekes and de Jonge [37] (subsection V-D). 

## _A. Pre-processing_ 

Prior to an analysis in LAMDA, the analyst needs to identify a _transition ensemble_ they are interested in. Our previous work, MolSieve [3], provides a workflow to achieve this, but in principle any method can be used as long as they meet LAMDA’s input requirements. There are no special interactions between MolSieve and LAMDA – experts simply export a transition region they are interested in and view it in LAMDA. LAMDA relies on a minimal amount of input data, which not only greatly reduces the amount of preprocessing that needs to be done before an analysis but also provides a great deal of flexibility. LAMDA expects two Pickle files per dataset: one that contains a Python dictionary of transition labels to a tuple of ASE Atoms objects; transition labels are tuples of state IDs that correspond to the initial and final states in the transition. The other file contains a dictionary of state IDs to matrices that represent per-atom features (subsection IV-A). The matrices for each individual state should be of dimension _n_ , the number of atoms in each state, by _k_ , the number of features. Additional scalar values can be imported to color the 3D visualizations throughout the system (subsection V-B); these values are not used for clustering. 

LAMDA begins pre-processing by computing the bond connectivity and distances between atomic positions for all of the unique states found in the transition ensemble. Afterward, the feature deltas, changes in bond lengths, and atomic 

6 

**==> picture [507 x 88] intentionally omitted <==**

**----- Start of picture text -----**<br>
Cluster Window<br>Reduction Window Selection Window<br>(c) Characterize the cluster (T2)<br>(a) Remove Duplicate  (b) Identify Families  (d) Evaluate cluster quality (T3) Scratchpad<br>Transitions &  Transitions of Transitions (T1) ee — (e) Insight provenance<br>Atomic Scalars Avg. intra-cluster distance<br>Structured Dataset<br>7g Se ee O B Label S S with Annotations<br>a ¢o<br>Original Reduced<br>**----- End of picture text -----**<br>


Fig. 3. An overview of LAMDA’s workflow. Initially, an ensemble of transitions and scalars of interest are provided as input. a.) Analysts interactively remove duplicate transitions in the ensemble and cluster them using the _Reduction Window_ . b.) Analysts examine the results using the dendrogram and the heatmap to identify broad groups of transitions ( **T1** ). The _Selection Window_ supports in-depth exploration of both clusters and transitions through clicking on the dendrogram and heatmap, respectively. (c. & d.) Clicking the dendrogram displays a _Cluster Window_ that provides views and interactions that characterize the cluster ( **T2** ) and help evaluate its quality ( **T3** ). e.) Transitions and clusters from elsewhere in LAMDA can be stored in the _Scratchpad_ , a centralized location for examining and organizing the analyst’s selections to generate insights that can be later exported. 

displacements are computed for each transition. The feature delta values are subsequently used to compute the distance matrix used for clustering. To do this, each transition’s _n_ by _k_ feature delta (∆ _f_ ; subsection IV-A) matrix is collapsed into a _k_ -dimensional feature vector by computing aggregate measures using the classic Coulombic potential energy function where the feature deltas can be conceptualized as pseudo-charges [38] ( _O_ ( _kn_[2] )); this ensures that the features are aggregated in a way that respects the overall structure of the transition while being invariant to rigid rotations, translations, or permutations of atoms. Afterward, the distance matrix is constructed by taking the _L_[2] norm between all feature vectors, followed by the ZCA-Whitening transformation [39], which de-correlates the result. This procedure guarantees that the distance between transitions is not sensitive to their absolute pose. 

Finally, LAMDA computes the global range for each scalar value, used when coloring visualizations to enforce visual consistency. Thanks to the power of ASE, LAMDA is highly flexible and can be used to analyze virtually any type of molecular dynamics simulation; however, we designed LAMDA around nanoparticles (i.e., systems with several hundred atoms), since they typically exhibit very complex state-to-state transitions compared to bulk systems, where geometric and energetic constraints typically limit the size and diversity of transitions. 

## _B. Transition Visualizations_ 

In this section, we introduce the various 3D visualizations for transitions found throughout LAMDA. There are three types of 3D visualizations supported by LAMDA: the _Atom Visualization_ , the _superquadric Visualization_ , and the _Group Displacement Visualization_ . The first two visualizations provide complementary perspectives on the changes to the system occurring during a transition ( **R1** ), while the _Group Displacement Visualization_ provides an overview for arbitrary sets of transitions, which LAMDA uses to represent clusters ( **R2** ). 

_a) Atom Visualization:_ This was our initial approach for visualizing transitions (cf. Figure 1,Figure 2), due to its use in popular tools such as OVITO [8]. Each atom is simply rendered in three-dimensional space as a sphere; a slider allows experts to interactively interpolate between the initial and final positions of a transition. Each sphere is colored 

using the _linear wcmr_ scale [36], which is indexed with the currently selected scalar value, set with a drop-down menu (defaults to average bond delta). The alpha channel corresponds to the scalar value, causing low values to become increasingly transparent as they approach the global minimum. Using transparency serves two purposes: it mitigates occlusion issues caused by atoms being surrounded by their neighbors, and it highlights regions of interest within a transition while reducing unnecessary information. Atoms with high delta values experience changes in their atomic neighborhood, regardless of the scalar chosen. 

While the _Atom Visualization_ is effective for analyzing single transitions, it requires significant effort to make sense of a group. We felt that we could capture displacements in a transition without relying on animations (i.e., the interpolation between initial and final positions of a transition). We retained this visualization because of its familiarity to domain experts, but these issues led us to exploring additional ways to visualize transitions. 

_b) superquadric Visualization:_ This approach (Figure 2, bottom; Figure 4, left) is designed to demonstrate the transformation of each atom’s neighborhood during a transition. Each atom is rendered as a superquadric [30], [32], which has a variable shape based on the eigen-system of its strain tensor (cf. subsection IV-B). These eigenvectors represent the principal strain directions. By default, _K_ 1 is used to color each atom according to the intensity of its extension (green) or contraction (pink) using the _gwv_ diverging colorscale [36]. The alpha value of each of element is set according to its intensity, with extreme values at either end of the scale being rendered as increasingly solid. Meanwhile, values approaching zero become increasingly transparent, eventually being replaced by small gray spheres to preserve structural information. superquadrics inherently encode the directional information of their deformation, thereby eliminating the need for temporal animations to illustrate displacements. 

_c) Group Displacement Visualization:_ This visualization (Figure 4, right) aims to combine the ease of interpretation provided by the _Atom_ visualization with the ability to examine multiple transitions at once. An attempt to simply plot the constituent atoms of a transition group on top of each other leads to severe clutter, making it difficult to track displacements. Instead, we aim to depict the overarching displacement theme 

7 

of the group based on the coherence between transitions in order to retain spatial information while maintaining visual scalability [40]. The _Group Displacement Visualization_ highlights atoms that were significantly displaced in a majority of the transitions within a group; the goal is to provide a quick way for analysts to identify major trends in a cluster ( **R2** ). 

To determine the atoms that need to be highlighted, the group’s _medoid_ transition _Tµ_ is first computed. The medoid transition is calculated using intra-group distances, simultaneously being used as a reference for aligning other transitions. 

Since atomic positions seldom conform perfectly in practice, even when aligned, we apply a Gaussian kernel to convert the initial atomic positions of all transitions within the corresponding group into a continuous space. We subsequently sample the displacement for every transition in the group at each position of _S_ 0 of the _medoid Tµ_ . This corresponds to an interpolation of the displacement using a radial basis function. We then average the results, obtaining **d**[˜] . 

This results in a vector field where displacement regions in phase within the selected group yield high values for _∥_ **d**[˜] _∥_ , while displacements in opposite directions cancel out. We also calculate a displacement correlation measure [41] and rescale it between zero and one, providing a quantitative measure of the overall conformation between displacement regions, readily adapted as a metric to judge the quality of a clustering ( **R3** ): 

**==> picture [204 x 27] intentionally omitted <==**

where **pi** is a position in _Tµ_ , **dt** is the displacement of transition **t** at **pi** , and _N_ is the number of transitions in the group. Finally, the initial atoms of the reference transition ( _S_ 0) are rendered together with arrows that indicate the average displacement direction for that position. Their colors ( _linear worb_ scale [36]) and alpha values are set corresponding to their correlation values. As with the _Atom Visualization_ , LAMDA supports interpolating between the initial and final values of the reference transition to provide additional visual context. 

Ultimately, our experiments found that the _Group Displacement Visualization_ is able to accurately capture the underlying theme of displacement in high-quality clusters. However, it often conveys less information with larger groups of transitions because the quality of the conformations tend to suffer when vastly different transitions are aligned, causing **d**[˜] to have low values. Thus, we note that the Group Displacement Visualization is sensitive to the quality of the input data used to generate the alignment and clusters; it can be used as a canary to indicate that a given clustering may be inadequate. To mitigate this issue, LAMDA provides a slider interaction to adjust a threshold value that controls how many atoms and arrows should be rendered; atoms below the threshold are rendered as small gray spheres to indicate their relative lack of movement. 

## _C. Reduction Window_ 

Practitioners begin their analyses with the _Reduction Window_ , which is designed to steer the results of the clustering. In this window, experts select a set of feature values to 

Fig. 4. A visual example of how three distinct transitions are aggregated into the _Group Displacement_ visualization. This visualization is intended to provide overviews for multiple transitions, facilitating intra-cluster comparisons ( **R2** ) and providing a visual marker for cluster quality ( **R3** ). Saturated colors indicate high displacement correlations between members, while gray spheres indicate the correlation for that point is below an adjustable threshold. 

**==> picture [252 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 3 5Export ScratchpadScratchpad<br>All<br>2<br>ICO<br>rotational<br>displacements<br>mm<br>Superquadric ▼ K1 ▼ ?<br>4 -0.2 0.0 0.2<br>▼<br>**----- End of picture text -----**<br>


Fig. 5. The _Selection Window_ , where experts can explore a transition ensemble organized by cluster. The dendrogram ( **1** ) is used to explore the dataset. Experts can click its branches to open a _Cluster Window_ to view individual transitions within their hierarchical context. The gray horizontal line is used to update the heatmap ( **2** ), which represents the distances between all transitions in the ensemble. The _Scratchpad_ ( **3** ) allows experts to organize and export their insights through a simple WYSIWYG editor ( **R4** ), adding annotations and grouping objects of interest together from selections made across the interface. ( **4** ) provides interactions that change the visualizations in the _Scratchpad_ ; ( **5** ) shows LAMDA’s export options ( **R5** ). 

generate a distance matrix (subsection V-A), which is subsequently reduced through an interactive _cleaning by clustering_ approach [42]. As mentioned in subsection IV-A, the features should reflect the local structure around an atom. A distance of zero between two sets of features indicates that the two transitions share a virtually identical structure. Since analysts are interested in only comparing unique transitions, all duplicates save one are removed. This can potentially improve the quality of the clustering relative to the full dataset; moreover, a smaller dataset translates to an overall lower cognitive burden of analysis as well as increased performance. 

The distance matrix is organized using agglomerative clustering with ward linkage. The reduction replaces all of the transitions within a cluster with its medoid (i.e., the transition that has the minimum summed distance to all of its neighbors). Analysts can steer the reduction by setting a cutoff value for the clustering; groups of transitions with distances below this value are removed. By default, this value is set to one; the reduction can be disabled with a value of zero. 

The _Reduction Window_ displays the full distance matrix as a 

8 

heatmap on the left-hand side, neighbored by another heatmap populated with the reduced matrix to the right, with a histogram above them (Figure 3). Both heatmaps are generated by reordering the distance matrices with the Bar-Joseph optimal ordering algorithm [43]; reordering the matrix in this manner places transitions that have low distances to each other nearby in the matrix and matches them to the way the dendrograms throughout the system are ordered. The heatmaps are fully interactive, supporting panning and zooming, which enables detailed inspection. 

To facilitate the search for an optimal cutoff value for the reduction, the original distance matrix displays groups that will be reduced as rectangles colored from white to black based on the average distances between its members. This causes groups with high distance values to sharply contrast the light colors of the heatmap, alerting the analyst to their presence. Meanwhile, the histogram grounds the color scheme by providing an abstract overview of the intra-cluster distances across all reduction groups. Analysts can use these two visual guides to quickly make a decision about the cutoff value. When a suitable reduction is found, the analyst can click the “Explore” button to open the _Selection Window_ . Analysts can return to this screen to readjust the reduction at any time. 

## _D. Selection Window_ 

The _Selection Window_ (Figure 5) displays an overview of the reduced dataset with a hierarchical heatmap and dendrogram (Figure 5.1-2). On the right, the _Scratchpad_ (Figure 5.3) is shown, which provides an interface for _insight provenance_ [9] ( **R4** ) and export. 

The dendrogram and heatmap provide overviews of the clustering ( **R1** ) and support interactions for detailed exploration. As mentioned previously, the dendrogram is colored using a dynamic color scheme [37]. This color scheme preserves the hierarchical structure within the coloring by recursively splitting the range of colors that child nodes in the tree can take. We initially used a linear categorical coloring scheme because of the huge number of different classes (i.e., each node in the tree would receive a different color). While this made it easier to distinguish leaf nodes, it was difficult to trace their ancestry in the hierarchy. The current color scheme preserves the hierarchy and has the added benefit of naturally capturing coarse clusters, but makes it far more difficult to differentiate between neighboring nodes; we discuss how we overcame this problem in subsection V-E. 

As in the _Reduction Window_ , the heatmap displays rectangles over leaf clusters. The cluster cutoff can be adjusted by dragging the gray line in the dendrogram up and down, which automatically updates the rectangles in the heatmap along with the colors of elements in the _Scratchpad_ (subsection V-F). To further aid high-level exploration, the x-axes of the dendrogram and heatmap are linked since they are ordered in the same way (subsection V-C). Panning around in one visualization automatically updates the other to provide a clear link between the dendrogram’s abstract representation and the low-level details contained in the heatmap. When the dendrogram is hovered, it also displays a tooltip showing the 

**==> picture [253 x 412] intentionally omitted <==**

**----- Start of picture text -----**<br>
? 5 Notes<br>1 ESTESSTEESTUESSSSESTUESR0E00oo0R"R- fe 2 Group Displacement<br>SOER RIES EE OO 000 CEE Oo SSE Oo nore | oe.<br>SOSSSSSBEPSOESUEESSESTSEEESOESSOEESSooORs,GSES 0 0000 SSS SSS SSSSS5550000e |" 6 see PyteeSy<br>BEEEEESEEOSUEEOESESFOOOEEEESETSOORNBOSSE SSSR SSS000SE00S000S00E0000EHR0R ')| "Sate.= ss. So - F. oe©<br>GEG SE SEESSS0SS0000000S0000000E0R08) | “woe * Gdeg A<br>SOCEPS ROE ESSSSCREESSEROBS000000000000 CEE COO SORE ROO 0S0000oo)Sor roon .es S x)hae<br>SEESGORE S ES SSRSRSESSASSESS Ee E SSER SSE SESSSS See Ee RSSSS eee E ee)Se oh-% RAMa@..¢)<br>SOREGEGEESSGOREOERPOPSGESSEESSEESS0SS0EGRGS00R5ES0S0E005BEES EES EERREESEERESESOS [EESSE]  CEES E EESSESSTEOOSSEESSESSSERS0RR OCCREEOCC [ RS] EBS [SESS0E0] SE0SCCGSSSEESSSe0S0E0005BOREOOOOBSBS DUCE OC SEER CCC EE COS PSSOOOOOe BECISS SeE [000530000] COSCOEE EEOOES CoreRCrooSSOC 0090E8SorrroTEaUCSen .|}|||| FSaveoe=e,hse 3 To Scratchpad 88  Correlation . 0.7<br>GEEEEPEPSCESSECEFEEREEEEEROSRCEEEE | @ st eP ee<br>GEEERESSSERESSERRSEEUS9S00095S000R | Og ad<br>BEEEEESCEETSESTEEEEESEESEEESEEREEEE | * Posse<br>BETSEESPEEESEESSSEESSEESSEEESEESOR | oe ass<br>SORRESOS0C B00 CCEA OO OSE AOOCroooS ¥ |<br>GOREHEPESHEPUEETEEESEESEEEEESEEEESESEEeEEHEES00EESEES0EROSS FCO 000 CECESOOS0e. EUS0ERSE POS Sec E 0RR8 rod - ! 4] ii<br>EREEBEGEESEPLEOESEEEEEEEEEEEEOEEEES | gees i | Ail<br>BEPEEEGCIETTEESTEOEEEEETSSESUSEooEE | PSP LE I {hi 4]<br>GEEERESEEEEOTEEEEEEERESSEEEESEOSESGOCEDUEEESSSOSoGEPEEESSEERSEESEEEESEEESESEeeoEeee~| EROSCTOUS SOS SSCORe ssBOSE oo0EE0ESooso!EEOSOCEne ||«ese|.«€t%:A ee® | mial} A | " iL4 ih ae" ll my | at<br>QEHEERR02!SSEOCSSCSPECS E OSOESNOOSSCSESBSE E ESBS ESE E EISDEB E S)L -__S>----~. 4 i re eee<br>. ef, ne ee oeeee Petre got ee<br>| cabs:e® oe weOy eeeead PAYWnas as,Sos HiMein (fairaedSeeiin 8<br>‘eeces|| SB yscs ||(gates: || dese’<br>Atom ▼ absAvgBonds ▼ t 0.0<br>0.0 |__| 0.02 0.04 Show Medoid isBhsosoaea eSHiner sean ba}cee SS)iiss)eB<br>Fig. 6. Cluster Windows allow for the detailed exploration of transitions<br>automatically clustered by LAMDA ( R1 ). The Embedding View ( 1 ) displays<br>transitions within a cluster as fully interactive 3D visualizations. Transitions<br>are organized in a 2D grid that reflects the overall cluster hierarchy. In this<br>figure, we include a zoomed-out overview of a grid from a large cluster and<br>annotate it with detailed visualizations to provide an illustrative example. The<br>Group Displacement Visualization ( 2 ) provides a 3D overview of a cluster<br>which facilitates analysis and comparisons ( R2; R3 ). The dendrogram ( 3 )<br>provides interactions to navigate the local cluster hierarchy. A heatmap ( 4 )<br>shows distances within the selected cluster; while ( 5 ) provides support for<br>annotations and note-taking.<br>current label of the cluster; this label can be edited in the<br>Cluster Window (subsection V-E). Most importantly, clicking<br>in either of the two overview visualizations allows analysts<br>to explore transitions and clusters in more detail: clicking<br>in the heatmap embeds the transitions corresponding to the<br>clicked cell in the  Scratchpad (subsection V-F), while clicking<br>branches in the dendrogram opens a Cluster Window .<br>**----- End of picture text -----**<br>


## _E. Cluster Windows_ 

_Cluster Windows_ (Figure 6) are designed for the in-depth analysis of a cluster and its constituent transitions. Transitions are aligned (subsection IV-A) to the cluster’s medoid transition prior to rendering to facilitate calculations and visual comparisons. The _Embedding View_ on the left (Figure 6.1) provides details about individual transitions ( **R2** ), while the views to the right (Figure 6.2-4) display overviews of the cluster’s transitions and provide visual cues towards cluster quality ( **R3** ). 

LAMDA supports opening multiple _Cluster Windows_ to facilitate comparison. While this is an unconventional approach, expert feedback suggests that being able to interact with only one window at a time would be a significant limitation (subsection VI-B). This is supported by the work of Plumlee and Ware [44], who argue that multiple windows should be used when complex patterns are being compared. This is especially relevant for our case, since we are comparing multiple complex patterns at once (i.e., the atomic displacement of hundreds of atoms across dozens of transitions). 

This window also supports navigating the cluster hierarchy. Left clicking branches in the dendrogram (Figure 6.3) switches 

9 

the window to show that particular node, while pressing _↑_ ascends the hierarchy to show the current cluster’s parent. Middle clicking a branch opens a new, independent cluster window. These interactions are mentioned in the help tooltip for this dendrogram. Moving the cluster cutoff line adjusts the colors throughout the window, although this may not be useful when examining very small clusters because lowlevel nodes are colored similarly (subsection V-D). With these general interactions in mind, we can turn our attention to the _Embedding View_ . 

The _Embedding View_ displays fully interactive 3D visualizations of the cluster’s transitions (subsection V-B) in 2D space. We initially tried organizing the visualizations by simply using the UMAP dimensionality reduction algorithm [45] with the cluster’s distance matrix as input, as well as using classic multi-dimensional scaling (MDS) algorithms [46]. Besides problems with interpretability posed by UMAP’s stochastic nature and the need to tune hyper-parameters, these embeddings suffered from multiple visual issues. Transitions would often be rendered on top of each other when they were highly similar – unfortunately, we realized that modifying the positions of the embedding could potentially affect their interpretation. Moreover, the embeddings created by these algorithms would often not match the hierarchical structure of the clustering, making it difficult to judge the quality of a given cluster. Finally, scrolling and panning around the embedding view made it difficult to compare individual transitions – experts would work around this by organizing transitions manually in the scratchpad, often placing them in a grid pattern. We realized that an intelligent grid layout could be computed automatically, which led to our current design. 

Naturally, simply placing transitions in a grid without considering their relationships would only solve the issue of occlusion. Instead, their grid positions are organized according to the cluster hierarchy using a Hilbert space-filling curve (SFC) [47]. The SFC can be viewed as a mapping from 1D to 2D; LAMDA uses the depth-first ordering of the dendrogram’s leaves as input to the SFC, which causes neighboring nodes and clusters to be placed near each other. Notably, this organizational scheme additionally mitigates the issue of neighboring nodes being colored similarly because their relationships are now encoded spatially. This is further supported by extensive visual linking, as hovering each transition highlights its position in any dendrogram it appears in (including other windows) and vice-versa. 

Inside the _Embedding View_ , the analyst can navigate the 2D space to get a closer look at transitions, individually adjust the 3D camera angle within each embedded view, change which type of visualization is being used to render the transitions, and adjust what step in the interpolation is being shown if supported by the currently selected visualization (i.e., the atom and displacement group visualizations). Changing the visualization is supported by a set of buttons, menus, and a slider directly below the _Embedding View_ (Figure 6.1). These adjustments instantly propagate to all visualizations in the window to facilitate comparisons, with the exception of individual 3D camera angles, which act independently. Among this set of controls is the “Show Medoid” button which 

highlights the medoid transition. This interaction is intended to provide more insight into the quality of the cluster ( **R3** ), as analysts can easily form an expectation of the medoid’s appearance based on the visualizations on the screen and compare it to the rest of the transitions in the group. 

We believe this view provides a solution to the problems presented by traditional transition analysis workflows because the smallest unit being displayed is now a transition instead of a single state and many transitions can be viewed at once. However, the grid layout can still make direct visual comparisons between transitions difficult if many transitions are being displayed. As such, this approach works best when multiple grids (i.e., cluster windows) can be displayed, and the analyst focuses on comparing smaller clusters side-by-side. We also warn that the analytical usefulness of the _Embedding View_ is highly dependent on the analyst’s input data, much like the clustering and its reduction. 

Cluster-level annotations can be added by clicking the “Notes” button (Figure 6.5; **R4** ) in the menu bar in the topright corner. This opens another window where analysts can rename the cluster to update the label shown whenever the cluster is interacted with. Additionally, a large text area is provided for writing detailed notes; we discuss how these annotations are exported in subsection V-G. 

We ultimately realized there was a need for a separate space to store insights gathered during the analysis. To this end, we developed the _Scratchpad_ , which supports intuitive notetaking interactions, thereby reducing the cognitive burden of comparing data from different clusters located on different screens. Double clicking transitions in the _Embedding View_ places them in the _Scratchpad_ ; clusters can also be embedded in the _Scratchpad_ by clicking the “To Scratchpad” underneath the _Group Displacement_ view (Figure 6.2). 

## _F. Note-taking with the Scratchpad_ 

As mentioned previously, the _Scratchpad_ (Figure 5.3) is meant for organizing insights ( **R4** ) that experts can refer to later. The _Scratchpad_ can be viewed as a simple electronic lab notebook [48] directly integrated into the interface. While lacking rich interactions, it enables analysts to store information in an intuitive manner. We deliberately chose to provide a minimal implementation due to the fact that developing a specific file format to store metadata and other information would quickly become obsolete [49]. Instead, LAMDA can generate a PDF report that captures their insights and directly provides access to the raw data files that analysts are interested in; additional metadata about the simulation can be included directly in the report through the Scratchpad’s editing capabilities. 

As with the _Embedding View_ , 3D visualizations are displayed in a 2D space, with several key differences: visualizations are positioned directly by the analyst, clusters can be embedded (via the “To Scratchpad” button in the cluster window), annotations can be directly added to the space, and arbitrary groups of transitions can be formed. Since the _Scratchpad_ does not inherently encode a cluster, transitions are not aligned prior to rendering and the “Show Medoid” button is not available. 

10 

A number of unique interactions in the _Scratchpad_ help organize the analyst’s thoughts ( **R4** ). Analysts can update the position of a visualization by clicking and dragging the middle mouse button. Double clicking on empty space in the _Scratchpad_ creates a textbox where annotations can be entered directly; holding the keyboard button **T** makes the text bold and is used to denote a title during export (discussed below). Analysts can further partition their findings by clicking and dragging in empty space, which draws a 2D rectangle. We refer to these as _visual groups_ , which are used during the export process. Finally, undesired elements can be removed using the right mouse button. Again, these interactions are explained in the help tooltip for the _Scratchpad_ . 

## _G. Export_ 

LAMDA provides two options for export: either by referring to the contents of the _Scratchpad_ to generate a custom folder layout or by simply using the clusters indicated by the current height cutoff in the dendrogram. Either option can be selected through the export menu in the _Selection Window_ (Figure 5.5), “Scratchpad” or “All”. 

Both methods of export mimic the hierarchical structure of the data and save transitions as Extended XYZ (.extxyz) files, a common format for molecular dynamics simulations. These files directly contain the atomic positions of the two states within a transition and can be directly used for further computations. Additionally, a PDF file containing the visual content of the scratchpad is created in the root folder. When “All” is selected, a folder is created recursively for each cluster according to the hierarchy set by the cluster cutoff (subsection V-D), with transition data being placed in leaf folders. If the analyst changed the title of a cluster, its folder is named accordingly, and any annotations created in the _Cluster Window_ are saved as plain-text files. The “Scratchpad” export option is designed to intuitively map the visual contents of the view to the file system. _Visual groups_ created by the analyst are exported as subdirectories that support nesting. Transition data is placed in its visual group’s folder, with transitions outside of visual groups being placed in the root-level folder. Text annotations are used either to name the corresponding folder (if in **bold** , created by pressing **T** while double clicking) or are placed in a plain-text file. 

## VI. CASE STUDY 

In this section, we demonstrate the efficacy of LAMDA through a case study conducted as a pair analysis [50] alongside our domain expert (E1) who is one of the coauthors on this paper. Our case study follows the expert while they examine a _transition region_ extracted from a simulation using MolSieve [3]. The original simulation describes a fixed-size nanoparticle (147 atoms) being subject to a constant temperature (700K) – in the literature, states from this kind of simulation are often referred to as the NVT (or canonical) ensemble. The experiment can be imagined as a nanoparticle floating around in a flask surrounded by a heat bath. 

nanoparticles are often studied due to their useful catalytic properties [51]. Since nanoparticles are small (at least one 

dimension is less than 100 nano-meters), they have a high surface area to volume ratio, making their structure susceptible to atomic rearrangements that occur when energy (in this case, heat) is applied to the system. These rearrangements can lead to significant structural changes which have a direct influence on the nanoparticle’s physical properties. 

The transition region we chose to study captures the nanoparticle changing from its initial stable face-centeredcubic (FCC) structure into an icosahedral structure (ICO). This structural transformation is well-studied [26], [52], [53] and is thus a good test-case for both our expert’s clustering approach and LAMDA. While our domain expert already knows _what_ is occurring during this part of the simulation, they would like to know _how_ it occurs. Of the eighteen million transitions contained in the original simulation, this _transition region_ contains about three thousand. While this is a significant reduction, it is still not amenable to manual analysis. 

Before they began, the expert computed feature matrices for each transition using the bi-spectrum components used as part of the Spectral Neighbor Analysis Potentials (SNAP) [54] approach, as computed by the FitSnap [27] package. They additionally used the adaptive Common Neighbor Analysis (CNA) [55] to assign structural labels per-atom in each state and then converted them to per-transition deltas to use as scalar values in the _Atom_ visualization (subsection V-B). The analyst believed that these values would help them quickly differentiate between clusters. Our expert aimed to investigate the behavior of the system and simultaneously evaluate how well SNAP features cluster, as they inherently encode physical deformations. 

## _A. Analysis_ 

The analyst started by selecting the SNAP features they computed in the _Reduction Window_ . Pre-processing took 4 minutes and 6 seconds total, 10 seconds being used to load the transition data (including scalar values, which are stored as separate files), 33 seconds for computing the transition invariants and 3 minutes and 26 seconds used to calculate the distance matrix. Once the distance matrix was computed, they examined the heatmap to gauge if the distances generated would cluster well. Noting large groups of distances close to zero, they experimented with different cutoff settings while referring to the heatmap and histogram to ensure the reduction would only remove identical transitions. They settled on a final cutoff value of 0.3, effectively removing nearly half of the dataset, leaving approximately one thousand four hundred transitions (Figure 5.2). When asked why they chose this value, they said the histogram in the _Reduction Window_ helped them make the decision, as most of the distances were binned at zero. 

The resulting distance matrix proved consistent with the analyst’s expectations due to the relatively long time-span of the transition region in the original simulation, as well as the fact that transition regions consist of lengthy periods of time where the system transitions back and forth between a number of stable states due to the high amount of energy needed to “break out” of a stable structure [26]. With the reduction complete, they opened the _Selection Window_ . 

11 

**==> picture [516 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
C1 C2 C3<br>pave ICO<br>Fast surface transformations ICO Rotational Minute deformations & Sane Slow diffusive motion<br>Fig. 7. Results from the case study. The dendrograms for each coarse cluster are displayed, labeled with its index and the expert’s interpretation; note that<br>they are not to scale. At the bottom, representative transitions for each cluster are shown, rendered with Group Displacement visualizations.  C 1 and  C 3 are of<br>particular interest, since they contain deformations that significantly alter the structure of the nanoparticle, with these two coarse clusters being separated by<br>their mechanism of action; they either deform the surface or internally re-arrange the structure of the nanoparticle. C 2 contains most of the transitions of the<br>dataset and is comprised of low-energy transitions that cause minute deformations on the surface, partitioned by magnitude.<br>**----- End of picture text -----**<br>


First, the analyst examined the dendrogram and moved its cutoff line to a y-position around 30 to focus on coarsegrained clusters (Figure 5.1-2). The clustering initially split the transition ensemble into three distinct clusters: _C_ 1 containing red, brown, and green clusters, _C_ 2 containing most of the dataset, and _C_ 3 containing purple-pink clusters (Figure 7). The analyst inferred that _C_ 1 and _C_ 3 contained structural changes because they were separated from the rest of the dataset. This set of interactions partially fulfills **R1** , as the analyst was able to generate a clustering quickly and discern which groups of transitions they were interested in exploring using the _Selection Window_ . 

The expert clicked on the red cluster to open a _Cluster Window_ . The expert immediately recognized that this cluster showed rearrangements occurring to icosahedral structures thanks to the _Group Displacement_ view (Figure 7, left). They noticed that the atomic displacements were highly correlated in the center of the system, indicating that the cluster contained highly similar transitions. Moreover, the shape of the _Group Displacement_ view resembled a nearly perfect icosahedral structure, implying that the transitions were also icosahedral. They were able to quickly confirm this by switching the selected scalar value shown in the Atom visualizations to the ICO delta count. This displayed a single central atom being highlighted in most of the _Atom_ visualizations. Some transitions did not have an ICO delta shown but were still grouped together with these transitions; to the analyst, it meant that the clustering was able to capture transitions occurring to structurally similar states that established methods (i.e., the CNA count) fail to recognize ( **R3** ). This also reflects the difficulty of such an analysis – numerical methods are still not enough to capture the complexities of atomic displacements. The analyst changed the title of the cluster to “ICO” and sent it to the scratchpad. Then, they went back to the _Selection Window_ to select the red cluster’s neighbors, brown and green. 

Here, the _Group Displacement_ view did not have any atoms that displayed a high correlation between transitions; this 

cluster was noticeably more diverse than the previous one. However, they noticed that the heatmap displayed two groups with low intra-cluster distances, one in each cluster. When the analyst reviewed the _Group Displacement_ visualizations for these groups, they noticed they were highly correlated along one direction on the surface down to the core of the nanoparticle (Figure 7, left); the analyst interpreted that these groups were both variations on fast surface transformations (FST) ( **R2** ). These types of transitions dramatically deform the surface of the nanoparticle and re-arrange its structure. With this in mind, they switched to the superquadrics visualization for all of the brown-green transitions. They noticed that the brown-green clusters differed in magnitude but otherwise were all examples of FSTs. The analyst attributed their discovery to the superquadrics pinpointing exactly where the atoms were moving the most without needing to track dozens of displacements ( **R1** ). Due to its distance, the analyst realized the “ICO” cluster also displayed FSTs. They visually confirmed this via the _Scratchpad_ and created a _visual group_ around the three clusters called “FST”. 

Before moving onto the purple-pink cluster on the other side of the dendrogram, the analyst noticed a small light blue cluster on the left side of _C_ 2. They opened a new _Cluster Window_ and adjusted the time slider to find they were all rotational displacements occurring to an icosahedral structure. These movements are sometimes accompanied by internal rearrangements within the system’s structure, which could be seen in the _Group Displacement_ view (Figure 7, center; **R2** ). The fact that these were clustered separately lent some level of credibility to the quality of the clustering, as this indicated that transitions weren’t simply being partitioned based on the magnitude of their movement alone. They sent this cluster to the Scratchpad and annotated it accordingly. 

The analyst turned their attention to the cluster furthest away from the ones they already investigated, avoiding the large cluster because they believed it would be full of lowenergy transitions. This is because transition regions often 

12 

are punctuated by transitions that oscillate between slight deformations of stable structures. This led them to open a new _Cluster Window_ for the set of purple-pink transitions. The transitions here seemed to affect the structure drastically but were mixed in terms of how dramatic the atomic displacements were. To understand this, they located a small group within the cluster that was highly similar and reviewed its _Group Displacement_ visualization. This revealed high correlations in the interior of the system which indicated that these transitions seemed to reconfigure atoms internally (Figure 7; right). 

The analyst wanted to compare this group and the FST group from before, so they opened a _Cluster Window_ for it. Just by moving the time slider back and forth, the difference was apparent – the FST group deformed the surface, while the new cluster would re-arrange atoms internally. The analyst annotated this set accordingly and sent it to the scratchpad. Finally, the analyst decided to take a look at the rest of the transitions in the ensemble; to do so, they pressed _↑_ to switch the _Cluster Window_ to show the entire dataset. 

The analyst was impressed by the fact that LAMDA remained responsive even though the entire dataset was rendered at once (Figure 6.1; **R6** ), one thousand four hundred fullyinteractive 3D visualizations were available for the analyst to explore in real-time. They zoomed in on the purple-pink clusters in the grid and investigated their neighborhood. They quickly switched through the various scalar values they created to view the other clusters; as expected, these did not contain transitions with internal structural reconfigurations. This was because most transitions did not contain atoms with deltas for either structural label, being rendered as gray spheres. Switching to the bond delta values did show a number of transitions that had moving atoms, but panning around and looking closely revealed that these were all surface level movements (Figure 7, center). The analyst did notice there were four transitions in the dark red cluster that exhibited rotational behavior because of how much their atomic bond deltas stood out in relation to their neighbors. They sent these transitions to the Scratchpad to examine them side-by-side. Ultimately, they found that these transitions did not meaningfully change the internal structure of the system (Figure 5.3). 

Upon reviewing their notes in the scratchpad, the analyst affirmed that the clustering was able to cluster transitions well ( **R4** ), separating surface movements from internal displacements by the types of structures they were occurring to. The pink-purple clusters contained transitions that reconfigured interior atoms, while the initial red, brown, green, light blue clusters contained transitions with dramatic surface transformations. Meanwhile, the middle clusters consisted of slight surface level deformations in the crystalline structure partitioned by magnitude. 

This case study demonstrates LAMDA’s exploratory capabilities. With LAMDA, our expert was able to quickly interpret the results of clustering transitions with SNAP potentials ( **T1** and **T2** ), becoming increasingly convinced of each cluster’s quality ( **T3** ) throughout the session. 

## _B. Expert Feedback_ 

We solicited feedback from the expert (E1) that performed the case study for suggestions on what other elements of the system could be improved. Since they were directly involved in the development of the system, we invited another domain expert (E2), a computational materials scientist with over a decade of experience, to simply interact with the system and evaluate its visual components. E2 did not have a dataset of their own to explore but was able to explore the data showcased in our case study. During both interviews, we discussed how LAMDA compared to their regular workflow and solicited feedback; their comments are interleaved to avoid redundancies. 

As we mentioned previously, domain experts typically investigate transition ensembles by manually sifting through data extracted by MolSieve with external visualization tools such as OVITO [8]. Since OVITO renders single atomic configurations, they typically load states in a sequence and flip back and forth between them to investigate atomic displacements. As such, both analysts found the _Atom_ visualization familiar and intuitive; they appreciated the ability to view multiple transitions at once, as well as the ability to interpolate between the beginning and end of transitions. However, E1 found that tracking multiple moving atoms across many transitions was difficult, which is why they turned to the _Superquadric_ visualization during the case study. E1 thought that the _Superquadric_ view was significantly more abstract, but found it helped them quickly pinpoint transitions of interest within a cluster. However, they found that this abstraction came at the cost of being able to discern atomic structures, causing them to switch between the visualizations as needed. E2 shared these concerns and added that the _Superquadric_ visualization required a significant amount of exposition before it could be understood. This suggests that future work could explore alternative abstractions for transitions using the lessons we learned here. 

Overall, both analysts were very pleased with LAMDA’s performance, both in terms of the system’s responsiveness and its streamlined analysis experience. Both experts found the _Embedding_ view valuable because it was able to simultaneously present a large amount of transitions at once and preserve the hierarchy of the clustering. E1 noted that comparing far-away transitions in one _Embedding_ view was difficult – they relied on opening multiple cluster windows to compare them side-by-side. Both experts appreciated the _Scratchpad_ , as it provided additional dimensions to their regular notes. E1 said, “I usually just sit and write things down if I find something, but adding a visual dimension to it really makes things clear, especially because it links right back to the data [when exported].” E2 said they often take screenshots and annotate them in another program. They thought that being able to interact with the transitions they saved was a significant improvement over static images. 

One major issue we have discussed throughout this work is the overlapping color scheme for clusters. When we asked E2 about it, they did not find it to be much of an issue – “They could be all black frames, the sorted grid solves this issue by 

13 

separating them by position so I can compare groups easily.” E1 echoed this sentiment, but noted that the color scheme could be confusing in the _Scratchpad_ where transitions and clusters are removed from their immediate context. 

When asked about potential improvements we could make, E1 suggested we could add support for visualizing pertransition scalar values, providing an additional dimension to compare clusters with. They provided an example from the case study: if we visualized the changes in potential energy per transition somewhere, the analyst would have easily identified _C_ 2 as a set of low-energy transitions. Another suggestion was enabling analysts to explore and compare multiple clusterings for one transition ensemble, which could help identify useful features and provide alternate perspectives. To add to this, they suggested the clustering itself should be editable through merge and difference operations, which could be used to manually improve cluster quality. E1 also mentioned they would like the time slider to be linked across windows, alongside the ability to control the camera for multiple windows in one interface rather than updating cameras individually. They also mentioned having the ability to hide the other plots in the Cluster Window as potentially being useful for side-byside comparisons. Finally, they suggested introducing a plugin system for analysts to experiment with different alignment and distance calculation algorithms, as well as general-purpose programmatic access to individual transitions within the system during run-time. 

We attempted to compensate for this by exaggerating the distortion of each glyph with constants, but it remains difficult to compare glyphs that slightly vary in value, especially when the values themselves are small. The issue we mentioned with structures being difficult to discern suggests that the perceptual trade-offs between concrete ( _Atom_ ) and abstract ( _Superquadric_ ) visualizations should be investigated in the context of scientific visualization. In a more general sense, addressing the issue of perceptually tracking multiple 3D objects across many visualizations is a promising and unexplored area of research. In terms of versatility, LAMDA was designed with materials molecular dynamics simulations in mind; therefore, our visualizations may not be easily interpretable for molecules that are very large or contain atoms with different elements, like the ones found in biological systems (e.g., proteins). To support the analysis of larger systems, specialized techniques that reduce and aggregate atomic displacement information will need to be developed. Supporting atoms with different elements, especially those with special interactions (e.g., forming functional groups) would require an entirely different set of techniques than the ones LAMDA provides. Finally, we do not claim that LAMDA is scalable, as we only tested the system with a little more than a thousand transitions being rendered at once. With this being said, LAMDA was built on the assumption that experts would be analyzing datasets around this size. 

## ACKNOWLEDGMENTS 

## VII. CONCLUSION 

In this work, we introduced a visual analytics system called LAMDA that facilitates the exploration and in-depth analysis of a set of transitions. Through its streamlined exploration process and coordinated views, experts are able to quickly catalog atomic behavior. The annotation features provide ways to organize their insights, directly linking with LAMDA’s powerful export features to help experts quickly iterate on new experimental code based on their interpretations. We verified LAMDA’s effectiveness through a case study, where an expert was able to identify and explore groups of atomic behavior within an ensemble of transitions exported from another tool. LAMDA is essentially a “last mile” analysis tool for molecular dynamics simulations: while other tools provide coarse descriptions of molecular behavior, LAMDA takes these coarse results and provides detailed insights down to individual transitions. The source code is available at https://github.com/rostyhn/LAMDA. 

We conclude with a discussion of some of LAMDA’s limitations that inform potential directions for future work. As we have already discussed, the color scheme still faces some issues with classes overlapping. One solution could be to implement an alternative dynamic color scheme such as the one proposed by Chen et al. [56]. Alternatively, we could experiment with glyphs that provide a unique visual fingerprint for each cluster using information from its transitions. We also found that the superquadric visualization needs improvement, as small variations in values did not translate to perceptible changes in length, key for comparing shapes [57]. 

The authors acknowledge the financial support provided by the Federal Ministry of Research, Technology and Space of Germany and by S¨achsische Staatsministerium f¨ur Wissenschaft, Kultur und Tourismus in the programme Center of Excellence for AI-research “Center for Scalable Data Analytics and Artificial Intelligence Dresden/Leipzig“, project identification number: ScaDS.AI 

## REFERENCES 

- [1] D. J. Wales and T. V. Bogdan, “Potential Energy and Free Energy Landscapes,” _The Journal of Physical Chemistry B_ , vol. 110, no. 42, pp. 20 765–20 776, Oct. 2006. 

- [2] M. E. Edwards, N. Kar, D. P. Freitas, L. Zhang, O. J. Wahab, L. A. Baker, S. E. Skrabalak, and X. Yan, “Size and shape effects on nanoparticlecatalyzed reactions enabled by high-throughput variable-temperature desorption electrospray ionization mass spectrometry,” _Analytical Chemistry_ , vol. 97, no. 36, pp. 19 544–19 551, 2025. 

- [3] R. Hnatyshyn, J. Zhao, D. Perez, J. Ahrens, and R. Maciejewski, “Molsieve: A progressive visual analytics system for molecular dynamics simulations,” _IEEE Transactions on Visualization and Computer Graphics_ , 2023. 

- [4] D. Duran, P. Hermosilla, T. Ropinski, B. Kozl´ıkov´a, A.[´] Vinacua, and P.-P. V´azquez, “Visualization of Large Molecular Trajectories,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. 25, no. 1, pp. 987–996, Jan. 2019. 

- [5] A. Jurcik, D. Bednar, J. Byska, S. M. Marques, K. Furmanova, L. Daniel, P. Kokkonen, J. Brezovsky, O. Strnad, J. Stourac, A. Pavelka, M. Manak, J. Damborsky, and B. Kozlikova, “CAVER Analyst 2.0: Analysis and visualization of channels and tunnels in protein structures and molecular dynamics trajectories,” _Bioinformatics_ , vol. 34, no. 20, pp. 3586–3588, Oct. 2018. 

- [6] R. Sk˚anberg, M. Linares, C. K¨onig, P. Norman, D. J¨onsson, I. Hotz, and A. Ynnerman, _VIA-MD: Visual Interactive Analysis of Molecular Dynamics_ . The Eurographics Association, 2018. 

14 

- [7] P. Ulbrich, M. Waldner, K. Furmanov´, S. M. Marques, D. Bedn´ˇr, B. Kozl´ıkov´, and J. Byˇska, “sMolBoxes: Dataflow Model for Molecular Dynamics Exploration,” _IEEE Transactions on Visualization and Computer Graphics_ , pp. 1–10, 2022. 

- [8] A. Stukowski, “Visualization and analysis of atomistic simulation data with ovito-the open visualization tool,” _MODELLING AND SIMULATION IN MATERIALS SCIENCE AND ENGINEERING_ , vol. 18, no. 1, 1 2010. 

- [9] E. D. Ragan, A. Endert, J. Sanyal, and J. Chen, “Characterizing Provenance in Visualization and Data Analysis: An Organizational Framework of Provenance Types and Purposes,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. 22, no. 1, pp. 31–40, Jan. 2016. 

- [10] H. Tsuzuki, P. S. Branicio, and J. P. Rino, “Structural characterization of deformed crystals by analysis of common atomic neighborhood,” _Computer Physics Communications_ , vol. 177, no. 6, pp. 518–523, Sep. 2007. 

- [11] G. J. Ackland and A. P. Jones, “Applications of local crystal structure measures in experiment and simulation,” _Physical Review B_ , vol. 73, no. 5, p. 054104, Feb. 2006. 

- [12] J. Behler, “Perspective: Machine learning potentials for atomistic simulations,” _The Journal of Chemical Physics_ , vol. 145, no. 17, p. 170901, Nov. 2016. 

- [13] T. Zubatiuk and O. Isayev, “Development of Multimodal Machine Learning Potentials: Toward a Physics-Aware Artificial Intelligence,” _Accounts of Chemical Research_ , vol. 54, no. 7, pp. 1575–1585, Apr. 2021. 

- [14] B. Mortazavi, X. Zhuang, T. Rabczuk, and A. V. Shapeev, “Atomistic modeling of the mechanical properties: The rise of machine learning interatomic potentials,” _Materials Horizons_ , vol. 10, no. 6, pp. 1956– 1968, 2023. 

- [15] L. Kocincov´a, M. Jareˇsov´a, J. Byˇska, J. Parulek, H. Hauser, and B. Kozl´ıkov´a, “Comparative visualization of protein secondary structures,” _BMC Bioinformatics_ , vol. 18, no. 2, pp. 1–12, Feb. 2017. 

- [16] S. Mehta, K. Hazzard, R. Machiraju, S. Parthasarathy, and J. Wilkins, “Detection and visualization of anomalous structures in molecular dynamics simulation data,” in _IEEE Visualization 2004_ , Oct. 2004, pp. 465–472. 

- [17] M. Mezei and M. Filizola, “TRAJELIX: A Computational Tool for the Geometric Characterization of Protein Helices During Molecular Dynamics Simulations,” _Journal of Computer-Aided Molecular Design_ , vol. 20, no. 2, pp. 97–107, Feb. 2006. 

- [18] R. Sk˚anberg, M. Linares, C. K¨onig, P. Norman, D. J¨onsson, I. Hotz, and A. Ynnerman, “VIA-MD: Visual interactive analysis of molecular dynamics,” in _Proceedings of the Workshop on Molecular Graphics and Visual Analysis of Molecular Data_ . Eindhoven: The Eurographics Association, Jun. 2018, pp. 19–27. 

- [19] A. Stukowski, “Visualization and analysis of atomistic simulation data with ovito–the open visualization tool,” _Modelling and simulation in materials science and engineering_ , vol. 18, no. 1, p. 015012, 2009. 

- [20] N. Cao, D. Gotz, J. Sun, and H. Qu, “DICON: Interactive Visual Analysis of Multidimensional Clusters,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. 17, no. 12, pp. 2581–2590, Dec. 2011. 

- [21] E. Karatzas, M. Gkonta, J. Hotova, F. A. Baltoumas, P. I. Kontou, C. J. Bobotsis, P. G. Bagos, and G. A. Pavlopoulos, “VICTOR: A visual analytics web application for comparing cluster sets,” _Computers in Biology and Medicine_ , vol. 135, p. 104557, Aug. 2021. 

- [22] E. J. Nam, Y. Han, K. Mueller, A. Zelenyuk, and D. Imre, “ClusterSculptor: A Visual Analytics Tool for High-Dimensional Data,” in _2007 IEEE Symposium on Visual Analytics Science and Technology_ , Oct. 2007, pp. 75–82. 

- [23] S. S. Thygesen, T. B. Masood, M. Linares, V. Natarajan, and I. Hotz, “Level of Detail Exploration of Electronic Transition Ensembles using Hierarchical Clustering,” _Computer Graphics Forum_ , vol. 41, no. 3, pp. 333–344, 2022. 

- [24] D. Perez, E. D. Cubuk, A. Waterland, E. Kaxiras, and A. F. Voter, “Longtime dynamics through parallel trajectory splicing,” _Journal of chemical theory and computation_ , vol. 12, no. 1, pp. 18–28, 2016. 

- [25] D. Perez, R. Huang, and A. F. Voter, “Long-time molecular dynamics simulations on massively parallel platforms: A comparison of parallel replica dynamics and parallel trajectory splicing,” _Journal of Materials Research_ , vol. 33, no. 7, pp. 813–822, 2018. 

- [26] R. Huang, Y. Wen, A. F. Voter, and D. Perez, “Direct observations of shape fluctuation in long-time atomistic simulations of metallic nanoclusters,” _Physical Review Materials_ , vol. 2, no. 12, p. 126002, 2018. 

- [27] A. Rohskopf, C. Sievers, N. Lubbers, M. Cusentino, J. Goff, J. Janssen, M. McCarthy, D. M. O. de Zapiain, S. Nikolov, K. Sargsyan, D. Sema, 

   - E. Sikorski, L. Williams, A. Thompson, and M. Wood, “Fitsnap: Atomistic machine learning with lammps,” _Journal of Open Source Software_ , vol. 8, no. 84, p. 5118, 2023. 

- [28] J. Lawrence, J. Bernal, and C. Witzgall, “A purely algebraic justification of the kabsch-umeyama algorithm,” _Journal of research of the National Institute of Standards and Technology_ , vol. 124, p. 1, 2019. 

- [29] P. M. Gullett, M. F. Horstemeyer, M. I. Baskes, and H. Fang, “A deformation gradient tensor and strain tensors for atomistic simulations,” _Modelling and simulation in materials science and engineering_ , vol. 16, no. 1, p. 17, 2008. 

- [30] G. Kindlmann, “Superquadric Tensor Glyphs,” in _Eurographics / IEEE VGTC Symposium on Visualization_ , O. Deussen, C. Hansen, D. Keim, and D. Saupe, Eds. The Eurographics Association, 2004. 

- [31] A. J. M. Spencer, _Continuum mechanics_ . Courier Corporation, 2004. 

- [32] D. Paschalidou, A. O. Ulusoy, and A. Geiger, “Superquadrics Revisited: Learning 3D Shape Parsing Beyond Cuboids,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2019, pp. 10 344–10 353. 

- [33] C. Stoiber, F. Grassinger, M. Pohl, H. Stitz, M. Streit, and W. Aigner, “Visualization Onboarding: Learning How to Read and Use Visualizations,” _OSF_ , Aug. 2019. 

- [34] S. Danisch and J. Krumbiegel, “Makie.jl: Flexible high-performance data visualization for Julia,” _Journal of Open Source Software_ , vol. 6, no. 65, p. 3349, 2021. [Online]. Available: https://doi.org/10.21105/joss.03349 

- [35] A. Hjorth Larsen, J. Jørgen Mortensen, J. Blomqvist, I. E. Castelli, R. Christensen, M. Dułak, J. Friis, M. N. Groves, B. Hammer, C. Hargus, E. D. Hermes, P. C. Jennings, P. Bjerre Jensen, J. Kermode, J. R. Kitchin, E. Leonhard Kolsbjerg, J. Kubal, K. Kaasbjerg, S. Lysgaard, J. Bergmann Maronsson, T. Maxson, T. Olsen, L. Pastewka, A. Peterson, C. Rostgaard, J. Schiøtz, O. Sch¨utt, M. Strange, K. S. Thygesen, T. Vegge, L. Vilhelmsen, M. Walter, Z. Zeng, and K. W. Jacobsen, “The atomic simulation environment-a Python library for working with atoms,” _Journal of Physics. Condensed Matter: An Institute of Physics Journal_ , vol. 29, no. 27, p. 273002, Jul. 2017. 

- [36] P. Kovesi, “Good Colour Maps: How to Design Them,” Sep. 2015. 

- [37] M. Tennekes and E. de Jonge, “Tree Colors: Color Schemes for TreeStructured Data,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. 20, no. 12, pp. 2072–2081, Dec. 2014. 

- [38] M. L. Cohen, “Pseudopotentials and Total Energy Calculations,” _Physica Scripta_ , vol. 1982, no. T1, p. 5, Jan. 1982. 

- [39] A. Kessy, A. Lewin, and K. Strimmer, “Optimal whitening and decorrelation,” _The American Statistician_ , vol. 72, no. 4, pp. 309–314, 2018. 

- [40] G. Richer, A. Pister, M. Abdelaal, J.-D. Fekete, M. Sedlmair, and D. Weiskopf, “Scalability in Visualization,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. PP, pp. 1–15, Dec. 2022. 

- [41] T. Vicsek and A. Zafeiris, “Collective motion,” _Physics Reports_ , vol. 517, 10 2010. 

- [42] W. Hu, A. Zaveri, H. Qiu, and M. Dumontier, “Cleaning by clustering: Methodology for addressing data quality issues in biomedical metadata,” _BMC Bioinformatics_ , vol. 18, no. 1, pp. 1–12, Dec. 2017. 

- [43] Z. Bar-Joseph, D. K. Gifford, and T. S. Jaakkola, “Fast optimal leaf ordering for hierarchical clustering,” _Bioinformatics_ , vol. 17, no. suppl 1, pp. S22–S29, Jun. 2001. 

- [44] M. D. Plumlee and C. Ware, “Zooming versus multiple window interfaces: Cognitive costs of visual comparisons,” _ACM Trans. Comput.Hum. Interact._ , vol. 13, no. 2, pp. 179–209, Jun. 2006. 

- [45] T. Sainburg, L. McInnes, and T. Q. Gentner, “Parametric UMAP Embeddings for Representation and Semisupervised Learning,” _Neural Computation_ , vol. 33, no. 11, pp. 2881–2907, Oct. 2021. 

- [46] A. Mead, “Review of the Development of Multidimensional Scaling Methods,” _Journal of the Royal Statistical Society. Series D (The Statistician)_ , vol. 41, no. 1, pp. 27–39, 1992. 

- [47] M. Wattenberg, “A note on space-filling visualizations and spacefilling curves,” in _IEEE Symposium on Information Visualization, 2005. INFOVIS 2005._ , Oct. 2005, pp. 181–186. 

- [48] M. Rubacha, A. K. Rattan, and S. C. Hosselet, “A Review of Electronic Laboratory Notebooks Available in the Market Today,” _JALA: Journal of the Association for Laboratory Automation_ , vol. 16, no. 1, pp. 90–98, Feb. 2011. 

- [49] H. K. Machina and D. J. Wild, “Electronic Laboratory Notebooks Progress and Challenges in Implementation,” _Journal of Laboratory Automation_ , vol. 18, no. 4, pp. 264–268, Aug. 2013. 

- [50] R. Arias-Hernandez, L. T. Kaastra, T. M. Green, and B. Fisher, “Pair analytics: Capturing reasoning processes in collaborative visual analytics,” in _Proceedings of the Hawaii International Conference on System Sciences_ . New York: IEEE, Jan. 2011, p. 10 pages. 

15 

- [51] M. Sharon, I. Nandgavkar, and M. Sharon, “Platinum nanocomposites and its applications: A review,” _Advances in Materials Research_ , vol. 6, no. 2, pp. 129–153, Jun. 2017. 

- [52] W. Gao, J. Wu, H. Park, J. Mabon, WL. Wilson, H. Yang, and J.-M. Zuo, “In Situ Observation of Pt Icosahedral Nanoparticles Transformation into FCC Single Crystal,” _Microscopy and Microanalysis_ , vol. 22, no. S3, pp. 766–767, Jul. 2016. 

- [53] W. Gao, J. Wu, A. Yoon, P. Lu, L. Qi, J. Wen, D. J. Miller, J. C. Mabon, W. L. Wilson, H. Yang, and J.-M. Zuo, “Dynamics of Transformation from Platinum Icosahedral Nanoparticles to Larger FCC Crystal at Millisecond Time Resolution,” _Scientific Reports_ , vol. 7, p. 17243, Dec. 2017. 

- [54] A. P. Thompson, L. P. Swiler, C. R. Trott, S. M. Foiles, and G. J. Tucker, “Spectral neighbor analysis method for automated generation of quantum-accurate interatomic potentials,” _Journal of Computational Physics_ , vol. 285, pp. 316–330, 2015. 

- [55] I. Filot, M. van Etten, D. Trommelen, and E. Hensen, “Bramble: adaptive common neighbor analysis (cna) for the recognition of surface topologies in nanoparticles,” _Journal of Open Source Software_ , vol. 8, no. 89, p. 5710, 2023. 

- [56] J. Chen, W. Yang, Z. Jia, L. Xiao, and S. Liu, “Dynamic Color Assignment for Hierarchical Data,” _IEEE Transactions on Visualization and Computer Graphics_ , vol. 31, no. 1, pp. 338–348, Jan. 2025. 

- [57] G. Qi and Z. Jing, “The quantitative research on length and area perception: A guidance on shape encoding in visual interface,” _Displays_ , vol. 75, p. 102325, Dec. 2022. 

