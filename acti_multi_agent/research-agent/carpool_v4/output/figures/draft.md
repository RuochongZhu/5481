% ============================================================
% CampusRide — Full Paper (v4.3)
% Compile: pdflatex → bibtex → pdflatex → pdflatex
% ============================================================
\documentclass[12pt]{article}

% ---------- Layout ----------
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\onehalfspacing

% ---------- Packages ----------
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{multirow}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage{natbib}
\usepackage{hyperref}
\hypersetup{
  colorlinks  = true,
  linkcolor   = blue!60!black,
  citecolor   = green!50!black,
  urlcolor    = blue!70!black,
}

% ---------- Convenience macros ----------
\newcommand{\campusride}{\textsc{CampusRide}}
\newcommand{\edudot}{\texttt{.edu}}
\newcommand{\researchagent}{\emph{research-agent}}
\newcommand{\finding}[1]{\textbf{F#1}}

% ============================================================
\title{CampusRide: An Identity-Verified Multi-Module Campus Platform\\and a Carpooling Case Study}
\author{Ruochong Zhu, Charlle Sy}
\date{April 2026}

\begin{document}
\maketitle

\begin{abstract}
\noindent
Small-town university campuses present a distinctive coordination challenge: commercial rideshare services are perceived as expensive and intermittently unavailable, yet students---especially international students---already coordinate rides, trades, and activities through informal messaging groups. This paper makes three contributions. First, we present \campusride{}, an identity-verified multi-module campus platform covering carpool, marketplace, activities, groups, messaging, and a cross-module points system, all built on a shared \edudot{} identity layer. Second, grounded in a formative survey ($N{=}111$ eligible, $44$ finished; 79\% Mandarin-native among those reporting native language), we report a deep-dive case on the carpool module. The survey reveals that all seven safety-related willingness-to-pay items exceed 50 on a 0--100 scale, that financial motivation dominates other incentive types, and---most distinctively---that a Driver/Both subset ($N{=}19$) exhibits the lowest tolerance for unfair ratings (mean\,$=$\,29.1) compared with late arrivals (47.2), destination changes (41.4), or non-standard routes (52.3), resonating with algorithmic-management concerns documented for professional gig workers. Third, we contribute \researchagent{}, an eight-phase thesis-conditioned evidence pipeline that produced an auditable literature base for this paper, including systematic contradiction surfacing for adversarial scoping. We discuss limitations including the absence of deployment evaluation, three-layer sample skew, and the risk that formalizing grassroots practices may reproduce platform-mediated harms.
\end{abstract}

\medskip
\noindent\textbf{Keywords:} campus platform, peer-to-peer carpooling, identity verification, rating fairness, formative survey, design case, evidence pipeline

\newpage

\section{Introduction}\label{sec:intro}

Ithaca, New York---home to Cornell University---is a small city where commercial rideshare availability is neither guaranteed nor affordable for students who commute within the city or travel to distant metropolitan areas during breaks. This framing extends beyond transportation: international students in such settings coordinate rides, buy and sell used goods, organize social activities, and seek information through a single social channel, typically a WeChat or WhatsApp group~\citep{Liu2023, Bonini2023}. The resulting \emph{campus coordination gap} is multi-faceted: it is not solved by a single-function app but rather calls for an integrated coordination infrastructure scoped to the campus community.

In this paper we address that gap from three angles. We conducted a formative survey of students in the Cornell/Ithaca area ($N{=}111$ eligible respondents, of whom 44 completed all questions; 79\% Mandarin-native among the 91 who reported native language) to understand transportation pain points, willingness-to-pay for safety and trust features, motivational structure, and driver-side tolerance for passenger-generated friction. Building on those findings, we designed and implemented \campusride{}, a six-module campus platform (carpool, marketplace, activities, groups, messaging, and points) whose modules share four design primitives: institutional identity verification, safety infrastructure, rating fairness, and gamification rewards. Finally, we developed \researchagent{}, an eight-phase evidence pipeline that supported the literature synthesis for this paper in an auditable, thesis-conditioned workflow.

We claim three contributions:
\begin{enumerate}[leftmargin=*, nosep]
\item A design case of an identity-verified six-module campus platform, demonstrating how a single \edudot{} identity layer and shared design primitives can structure coordination infrastructure across campus-relevant domains.
\item A formative, survey-grounded deep-dive into the carpool module, surfacing three transferable design observations: \edudot{} verification as a trust primitive, grassroots coordination practices among international students, and a counterintuitive sensitivity of occasional campus drivers ($N{=}19$) toward rating fairness.
\item \researchagent{}, a thesis-conditioned eight-phase evidence pipeline that provides an auditable literature synthesis workflow, contributed as a reusable methodology tool for the design-research community.
\end{enumerate}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_bdd_system_context.pdf}
  \caption{Block Definition Diagram (BDD) of \campusride{} v4.4 in context. The «system» block (centre) lists six modules and 184 verified users; five «actor» blocks (left) and seven «external system» blocks (right) connect via labeled interaction edges (e.g.\ JWT-authenticated REST + Socket.IO, Resend verification mail, 82 WeChat outreach pushes). The Uber/Lyft block is rendered as a competitor reference rather than an integration. Snapshot 2026-04-23.}
  \label{fig:mbse-bdd}
\end{figure*}

\section{Related Work}\label{sec:related}

We organize the literature around three lines: the small-town campus coordination gap that motivates the platform (\S\ref{sec:rw-gap}), the grassroots practices and integrated-platform research that justify multi-module design (\S\ref{sec:rw-grassroots}), and the four design primitives that the platform operationalizes (\S\ref{sec:rw-primitives}).

\subsection{Small-Town Campus Transportation and Coordination Gaps}\label{sec:rw-gap}

A transportation coordination gap exists across university and small-city settings: mobility needs are local, recurrent, and socially embedded, yet available services are fragmented across campus shuttles, sparse public transit, and commercial rideshare~\citep{Khan2023, ChagnonLessard2021}. Campus-transit satisfaction studies document that service quality and schedule alignment vary substantially across institutions, pointing to structural friction rather than incidental inconvenience~\citep{Khan2023}. In sparsely populated areas, shared first- and last-mile systems are treated as service-design challenges rather than solved markets~\citep{Pecherski2025}, and meta-analytic work on Mobility-as-a-Service deployments suggests that integrated mobility systems can improve accessibility but that the evidence is not campus-specific~\citep{Witlox2024}. This framing resonates with our formative survey, where Uber was often described as expensive (28 of 32 respondents selecting ``Slightly higher'' or ``Much higher'') and sometimes unavailable or unreliable (23 of 32 reporting at least moderate difficulty), though we return to that evidence in \S\ref{sec:findings-passenger}.

A service gap by itself does not justify a peer platform. Sharing-economy research documents why peer exchange can be viable when trust cues, participation incentives, and fairness perceptions are designed carefully~\citep{Ert2016, Blut2024, Broeder2023}. Peer-to-peer carpooling studies indicate that trust-building mechanisms have differential effects depending on car ownership and user experience~\citep{Hartl2025}, and crisis-period comparisons between Airbnb and Uber suggest that trust dynamics are platform- and context-dependent~\citep{Amrollahi2024}. Crucially, the gap extends beyond transportation: students in small-town campuses face coordination friction in secondhand trading, event organization, and everyday social coordination, which together form a broader \emph{campus coordination gap} that motivates a multi-module platform rather than a single-function carpooling app. Most of the trust literature, however, originates from Airbnb or general sharing-economy platforms, so the case for a campus-scoped peer-rides system is motivated rather than fully established by prior work alone.

\subsection{Grassroots Coordination and Integrated Campus Platforms}\label{sec:rw-grassroots}

Studies of overseas students and adjacent mobile-messaging contexts document that everyday platforms such as WeChat and WhatsApp already carry practical coordination, risk management, and help-seeking across borders~\citep{Liu2023, Shi2018, Jin2021}. Chinese overseas students assemble ``mobility repertoires'' under constraint, deploying distributed social ties for information, emotional support, and logistical coordination~\citep{Liu2023}. Mobile instant messaging is documented as boundary-crossing infrastructure for informal problem-solving and knowledge exchange~\citep{MobileIM2018}, and private messaging groups expand into mutual aid, resistance, and community-of-practice functions when formal platforms leave coordination gaps~\citep{Bonini2023}. In our formative survey, 17 of 72 Mandarin-native respondents reported using WeChat or WhatsApp groups to find carpool partners, compared with 1 of 15 English-native respondents (or, within the smaller subset who answered the carpool-finding question, 17 of 21 vs.\ 1 of 2). While we frame this as a resonance with the literature rather than confirmation, the direction is consistent: messaging-based coordination is an active, everyday practice among international students.

This coordination is not limited to rides. The same WeChat groups serve as channels for secondhand trading, event announcements, information sharing, and emergency assistance~\citep{You2023, Chen2024wechat, ShamirTixell2022}. Students already depend on a single social channel for multi-domain coordination, providing an experiential anchor for the legitimacy of a multi-module platform.

A smaller body of super-app research indicates an emerging design space for closed-community integration within otherwise mass-market platforms. KakaoTalk chatrooms function as bounded ``dwelling places'' with primary, secondary, and tertiary social regions~\citep{Kim2015kakao}; LINE serves as intergenerational infrastructure inside Japanese family units~\citep{Ohashi2017line}; and nurse-facilitated patient groups inside WeChat operate as closed clinic-scoped coordination infrastructure~\citep{Wang2020wechat}. Platform-studies work on super-app platformization provides a theoretical backdrop~\citep{Steinberg2020line}. This literature indicates that bounded-scope multi-module coordination is a plausible design target, but a systematic treatment at the campus level is less developed---\campusride{} contributes one case within this emerging space. Because existing work only partially explains how a campus-scale system should be composed, we next distill design primitives rather than inheriting a ready-made platform blueprint.

\subsection{Design Primitives: Identity, Safety, Rating Fairness, and Rewards}\label{sec:rw-primitives}

We distill four design primitives from the literature, presenting them in parallel without value-ranking; the empirical findings in \S\ref{sec:findings} and the design decisions in \S\ref{sec:design} perform the ranking work.

\paragraph{Identity.} Identity verification in sharing-economy contexts has a mature literature~\citep{Li2020trust, Ert2016}. We specialize this to institutional and \edudot{}-scoped contexts, where closed-community scoping can reduce stranger-coordination costs. The foundational evidence comes from Facebook's \edudot{}-gated era: college students' use of the then-closed network was positively associated with bridging social capital~\citep{Ellison2007}, and institutionally seeded network ties enabled resource mobilization among college cohorts~\citep{Ellison2014}. Campus-bounded anonymous platforms such as Yik Yak further demonstrate that geographic or institutional scoping functions as a trust-relevant identity primitive even without explicit credential verification~\citep{Schlesinger2017, Black2016, Heston2016, Wu2017}.

\paragraph{Safety.} Platforms can reduce uncertainty during a trip through real-time location sharing, SOS escalation, and shared situational awareness~\citep{Ali2024carpool, Divya2025}. A women-only immunization carpool in rural Pakistan demonstrated that transport coordination can be paired with explicit protective infrastructure~\citep{Ali2024carpool}. Peer ride-sharing design work emphasizes coordination and safety features over ratings, suggesting that amateur-driver settings may govern trust through different levers than professional gig platforms~\citep{RiderConnect2026}.

\paragraph{Rating fairness.} Reputation systems coordinate trust, but recent work increasingly asks who is disadvantaged by biased feedback, asymmetric visibility, or platform-side promotion rules~\citep{Tushev2022, Christiaens2025}. Anti-discrimination design strategies document that sharing-economy platform features can trigger discrimination and that specific software design strategies can mitigate it~\citep{Tushev2022}. Platform-level fairness dynamics under biased ratings show that promotion policies can counteract rating-based discrimination~\citep{Smit2026}. Importantly, existing rating-fairness literature primarily covers professional gig workers; whether amateur or occasional drivers exhibit similar rating anxiety is a question we pursue in \S\ref{sec:findings-driver}.

\paragraph{Rewards.} Gamification is commonly discussed as a behavioral design layer that can sustain participation and pro-social mobility choices~\citep{Galeote2021, Zhang2023ant, Vacondio2025}. We treat it as a parallel lever with different behavioral aims than identity, safety, or fairness---not as a substitute for them.

\section{Methodology}\label{sec:method}

\subsection{Formative Survey Protocol}\label{sec:method-survey}

We distributed an online survey via Qualtrics to students in the Cornell University and broader Ithaca area between February and March 2025. Participation was voluntary and anonymous; informed consent was obtained at the start of the survey. The survey platform recorded $N{=}117$ response entries, of which six were internal test responses (Status\,$=$\,``Survey Preview'') that we excluded, leaving $N{=}111$ eligible respondents. Of these, $N{=}44$ completed all questions (approximately 40\% completion rate).

Among the 91 respondents who reported their native language, 72 (79\%) indicated Mandarin Chinese, 15 (16\%) indicated English, and 4 (5\%) indicated other languages. We disclose this distribution as scope: our findings are most directly grounded in the experience of Mandarin-speaking international students, and we caution against generalizing to the broader campus population. Self-reported travel roles were: Rider ($N{=}56$), Driver ($N{=}23$), Both ($N{=}22$), and unreported ($N{=}10$).

The survey covered seven modules: demographics, travel patterns, pain points, Uber perception (pricing and availability), willingness-to-pay for safety features (seven items on a 0--100 slider), motivational structure for carpooling (four items on a 0--100 slider), and driver-side tolerance for passenger-generated friction (four items on a 0--100 slider). All analyses are descriptive; we report no inferential statistics, no $p$-values, and no significance claims. Each finding is reported with the per-item~$N$.

\subsection{Literature Synthesis via Research-Agent}\label{sec:method-pipeline}

The literature base for \S\ref{sec:related} and \S\ref{sec:discussion-limits} was assembled using \researchagent{}, an eight-phase thesis-conditioned evidence pipeline. The pipeline progresses through corpus assembly (OpenAlex, Semantic Scholar, arXiv, Lens, Crossref), classification into a ten-category taxonomy (A--J), deep extraction, relationship-graph construction with evidence-sufficiency diagnostics, narrative-chain generation, contradiction mapping, evidence-inventory compilation, and five-reviewer evaluation. Its direct value to this paper is twofold: an auditable contradiction-surfacing process that shaped our adversarial scoping (\S\ref{sec:discussion-limits}), and evidence-sufficiency diagnostics that flagged under-covered categories requiring manual supplement. The architecture and application are detailed in \S\ref{sec:pipeline}; the full implementation, configuration, and audit logs are open-sourced at the project repository. We describe the pipeline as an \emph{evidence-chain organization tool}, not as an automated thesis generator or open-ended gap-discovery mechanism.

\section{Formative Survey Findings}\label{sec:findings}

\subsection{Passenger-Side: Transportation Gap, WTP, and Motivations}\label{sec:findings-passenger}

\paragraph{Transportation-gap quantification (\finding{1}).} Among the 32 respondents who answered the Uber-pricing question (Q16), 28 (88\%) selected ``Slightly higher'' or ``Much higher than other cities.'' Among the 32 who rated Uber availability (Q23), 23 (72\%) selected ``Moderate,'' ``Somewhat difficult,'' or ``Very difficult.'' These numbers quantify a perceived gap but do not constitute a causal claim about market failure.

\paragraph{Distance- and role-conditioned pain-point structure (\finding{1b}).} Beyond the Uber-specific gap above, we asked respondents to rate eight categories of travel issues---inflexible schedule, bus delays, expensive parking, weather disruptions, limited coverage, luggage restrictions, safety hazards, and inconsistent operating hours---across three distance scenarios. Figure~\ref{fig:severity-radar} disaggregates the responses by travel role and distance scenario. We frame this as a directional observation rather than a quantitative claim: per-cell $N$ ranges from $3$ to $7$, below conventional thresholds even for descriptive design-research reporting. The coarse pattern is that role-specific concerns concentrate at shorter distances---Driver/Both respondents foreground weather disruptions and expensive parking within Ithaca, while Rider-only respondents foreground limited coverage and inconsistent operating hours---and partially converge at the long-distance end, where limited coverage emerges as a shared concern. This distance-conditioned convergence is consistent with the carpool module's prioritization of long-distance trip matching (see \finding{6} below and \S\ref{sec:carpool-overview}).

\begin{figure}[ht]
  \centering
  \includegraphics[width=\linewidth]{pic/q30_severity_by_distance.pdf}
  \caption{Severity of eight travel-issue categories across three distance scenarios, grouped by travel role. Higher values indicate greater perceived severity. Driver/Both subset $N{=}3$--$5$ per axis (red solid); Rider-only subset $N{=}3$--$7$ per axis (blue dashed). Per-cell sample sizes are small; the figure is reported as a directional pattern rather than a quantitative finding.}
  \label{fig:severity-radar}
\end{figure}

\paragraph{Willingness-to-pay for safety features (\finding{3}).} Seven safety-related features were each rated on a 0--100 slider indicating the percentage by which each feature would increase the respondent's willingness to use a carpooling service (Table~\ref{tab:wtp}). All seven items exceeded a mean of 50, with real-time location sharing (mean\,$=$\,69.1, median\,$=$\,76) and \edudot{} school-email verification (mean\,$=$\,67.3, median\,$=$\,79) as the top two.

\begin{table}[ht]
  \centering
  \caption{Willingness-to-pay uplift for seven safety features (0--100 scale). Items sorted by mean.}\label{tab:wtp}
  \smallskip
  \begin{tabular}{@{} l r r r @{}}
    \toprule
    Feature & $N$ & Mean & Median \\
    \midrule
    Real-time location sharing       & 31 & 69.1 & 76 \\
    School email verification (\edudot) & 31 & 67.3 & 79 \\
    Emergency SOS button             & 30 & 63.5 & 64 \\
    Driver experience visibility     & 31 & 60.5 & 60 \\
    Auto trip-sharing w/ contacts    & 30 & 55.4 & 52 \\
    Driver social connections        & 30 & 54.9 & 60 \\
    Interior car photos              & 30 & 50.9 & 52 \\
    \bottomrule
  \end{tabular}
\end{table}

We observe that all seven items cross the 50-point threshold and that the top four items have medians at or above 60, indicating broadly positive disposition toward safety-related features in peer carpooling.

\paragraph{Motivation structure (\finding{4}).} Four motivation items were rated on a 0--100 slider. The aggregate results exhibit a two-tier structure: splitting fuel costs leads at 63.6 ($N{=}31$), followed by a cluster of platform rewards/gamification at 48.3 ($N{=}24$), social network expansion at 45.6 ($N{=}26$), and environmental impact at 44.5 ($N{=}24$). Financial motivation is the dominant driver, while gamification, social, and environmental motivations form a secondary tier at roughly comparable levels. Disaggregated by travel role (Figure~\ref{fig:motivation-radar}), the Driver/Both subset rates platform rewards and social expansion appreciably higher than the Rider-only subset, while the Rider-only subset rates environmental impact slightly higher; both subsets converge on splitting fuel costs as their top motivation. This role split is consistent with the platform's gamification design (\S\ref{sec:dd-gamification}), in which points serve primarily as a driver-side incentive lever rather than as a substitute for the dominant cash-splitting motivation.

\begin{figure}[ht]
  \centering
  \includegraphics[width=0.72\linewidth]{pic/q26_motivation_radar.png}
  \caption{Carpooling motivation by travel role (0--100 scale; higher\,$=$\,stronger motivation). Driver/Both subset $N{=}15$ (red solid) and Rider-only subset $N{=}7$ (blue dashed). Driver-side respondents rate platform rewards and social expansion higher than Rider-only respondents; Rider-only respondents rate environmental impact slightly higher; both subsets converge on splitting fuel costs as the dominant motivation.}
  \label{fig:motivation-radar}
\end{figure}

\paragraph{Driver supply willingness (\finding{6}).} Among 33 respondents who answered the driver supply-willingness questions (Q23\_1--Q23\_3), the proportion selecting ``Very willing'' or ``Extremely willing'' was: in-Ithaca trips 10/33 (30\%), short-distance trips 9/33 (27\%), and long-distance trips 12/33 (36\%). Long-distance trips attracted the highest supply willingness, which directly informs the carpool module's prioritization of long-distance trip scenarios in \S\ref{sec:carpool-overview}.





\subsection{Driver-Subset Tolerance and the Rating-Fairness Asymmetry}\label{sec:findings-driver}

This subsection reports the paper's most distinctive finding. We analyze driver-side tolerance for passenger-generated friction on Q24 (four items, each on a 0--100 slider where higher values indicate greater tolerance).

\paragraph{Subset selection rationale.} Q24 items are phrased as ``As a driver, how tolerant would you be of\ldots'' Respondents who self-identified as Rider-only answered this question hypothetically, lacking actual driving experience to calibrate their responses. Mixing hypothetical and experience-based answers in a single analysis would dilute the signal from actual drivers. We therefore report Q24 results separately for two subsets: (a)~the \emph{Driver/Both subset} (per-item $N{=}17$--$19$, with $N{=}17$ for the strict intersection of respondents who completed all four items), comprising respondents who self-reported as Driver or Both; and (b)~the \emph{Rider-only control} (per-item $N{=}11$--$12$). The modal sample size in CHI-published work is $N{=}12$~\citep{Caine2016}; our $N{=}19$ descriptive observation falls within the CHI local-standards distribution for formative design research.

\paragraph{Core finding (\finding{5}).} Table~\ref{tab:tolerance} presents the four tolerance items across both subsets using per-axis $N$, while Figure~\ref{fig:tolerance-radar} visualizes the same pattern as a four-axis radar over the strict intersection of respondents who completed all four items.

\begin{table}[ht]
  \centering
  \caption{Driver tolerance for passenger-generated friction (0--100 scale; higher\,$=$\,more tolerant). Bold highlights the lowest item within each subset.}\label{tab:tolerance}
  \smallskip
  \begin{tabular}{@{} l rr rr @{}}
    \toprule
    & \multicolumn{2}{c}{Driver/Both} & \multicolumn{2}{c}{Rider-only} \\
    \cmidrule(lr){2-3}\cmidrule(lr){4-5}
    Tolerance item & $N$ & Mean & $N$ & Mean \\
    \midrule
    Passenger late 10\,min (Q24\_1)    & 19 & 47.2 & 12 & 35.7 \\
    Destination change (Q24\_2)        & 19 & 41.4 & 12 & 19.6 \\
    \textbf{Unfair rating (Q24\_3)}    & 19 & \textbf{29.1} & 11 & 22.4 \\
    Non-standard route (Q24\_4)        & 17 & 52.3 & 11 & 33.2 \\
    \bottomrule
  \end{tabular}
\end{table}

\begin{figure}[ht]
  \centering
  \includegraphics[width=0.72\linewidth]{pic/q24_tolerance_radar.png}
  \caption{Driver tolerance for passenger-generated friction (0--100 scale; higher\,$=$\,more tolerant), grouped by travel role. The radar uses the strict intersection of respondents who completed all four Q24 items: Driver/Both $N{=}17$ (red solid) and Rider-only $N{=}11$ (blue dashed). Per-axis means in Table~\ref{tab:tolerance} use slightly looser per-item dropna and therefore differ marginally from the radar values. The Driver/Both polygon contracts visibly along the ``unfair rating'' axis (top) relative to the other three friction items, while the Rider-only control shows no comparable asymmetry.}
  \label{fig:tolerance-radar}
\end{figure}

Within the Driver/Both subset, ``unfair rating'' tolerance (29.1) is 12.3 to 23.2 points lower than the other three items (41.4--52.3). Counterintuitively, the least-tolerated disruption is not passenger behavioral misbehavior---arriving late, changing destinations, or requesting unusual routes---but unfairness from the rating system itself. The asymmetry is the visual signature of Figure~\ref{fig:tolerance-radar}: the ``unfair rating'' axis at the top of the radar contracts inward relative to the other three axes. In the Rider-only control, ``unfair rating'' (22.4) is not distinctly the lowest (``destination change'' at 19.6 is lower), confirming that the distinctive rating-fairness asymmetry is anchored in the Driver/Both subset. This difference is precisely why the full-sample mixed report ($N{=}30$) is not the methodologically appropriate headline.

\paragraph{Literature dialogue.} Algorithmic-management research has documented professional gig workers' anxiety toward platform rating systems~\citep{Keegan2025, Kinowska2022}. Our observation resonates with this concern in a smaller-scale, higher-trust, non-professional campus peer-carpool setting. Two implications follow. First, even with \edudot{} identity verification as a strong trust signal, the fairness of the rating system itself remains an independent, non-substitutable design concern. Second, rating anxiety is not exclusively a product of professional-labor bargaining: a small but growing peer-to-peer carpool literature documents similar concerns among amateur drivers in carsharing and carpooling settings~\citep{Neifer2023, Hartl2025}, and our Driver/Both-subset observation parallels this emerging pattern. Field experiments on two-sided reputation systems further document that the two sides of a peer marketplace respond asymmetrically to rating-system architecture~\citep{Fradkin2021}, though those studies use an economic fairness framing distinct from our HCI design-research perspective. Whether the sensitivity observed here is isomorphic to gig-worker rating anxiety remains an open question; we treat this as a formative design signal, not a confirmed replication.


\section{\campusride{} Platform Design}\label{sec:design}

\subsection{Platform Overview and Shared Design Primitives}\label{sec:design-overview}

\campusride{} is built on a Vue~3 + Express + Supabase + Socket.IO stack. Six modules---carpool, marketplace, activities, groups, messaging, and points---share four design primitives distilled in \S\ref{sec:rw-primitives}: institutional identity verification, safety infrastructure, rating fairness, and gamification rewards. Table~\ref{tab:primitives} shows how each module engages these primitives.

\begin{table}[ht]
  \centering
  \caption{Design-primitive engagement across modules. \checkmark\checkmark\,$=$\,intensive; \checkmark\,$=$\,present; $\circ$\,$=$\,not applicable.}\label{tab:primitives}
  \smallskip
  \begin{tabular}{@{} l cccc @{}}
    \toprule
    Module & Identity & Safety & Rating & Rewards \\
    \midrule
    Carpool       & \checkmark & \checkmark\checkmark & \checkmark\checkmark & \checkmark \\
    Marketplace   & \checkmark & $\circ$               & \checkmark            & \checkmark \\
    Activities    & \checkmark & $\circ$               & $\circ$               & \checkmark \\
    Groups        & \checkmark & $\circ$               & $\circ$               & $\circ$ \\
    Messages      & \checkmark & $\circ$               & $\circ$               & $\circ$ \\
    Points        & \multicolumn{4}{c}{\emph{(cross-module meta-layer)}} \\
    \bottomrule
  \end{tabular}
\end{table}

The \edudot{} identity layer serves as the shared admission gate for all modules; the points module functions as a cross-module meta-layer; and the carpool module exercises all four primitives at maximum intensity, which---combined with the long-distance driver supply willingness finding (\finding{6})---is why we select it for deep-dive analysis.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_ibd_system_internals.pdf}
  \caption{Internal Block Diagram (IBD): six modules in a 3$\times$2 grid over four shared substrate bars (\edudot{} identity, Notification + Socket.IO, Supabase + RLS, WeChat outreach pipeline). Inter-module port-flows include Carpool$\rightarrow$Messages (\texttt{ride\_carpool} group on first booking), Marketplace$\rightarrow$WeChat (62 outreach pushes), and Activities$\rightarrow$Points (geo-checkin reward, currently inert). The Points overlay ring expresses its cross-module meta-layer role rather than placement on a 6-vertex grid (\S\ref{sec:points-overview}).}
  \label{fig:mbse-ibd}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_class_diagram_db.pdf}
  \caption{UML Class Diagram for the production database schema (snapshot 2026-04-23). Fifteen core classes are grouped into six domain clusters (Identity, Carpool, Activities, Marketplace, Messaging, Cross-module). Associations carry UML multiplicity labels (\texttt{1}, \texttt{0..1}, \texttt{1..*}, \texttt{0..*}); aggregation ends are marked with open diamonds on the owning side. The polymorphic \texttt{wxgroup\_notice\_record (source\_type, source\_id)} relation to \texttt{Ride}\,/\,\texttt{MarketplaceItem}\,/\,\texttt{Activity} is rendered as an annotated note rather than three near-identical edges to keep the layout legible.}
  \label{fig:mbse-class-db}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_ffbd_platform.pdf}
  \caption{Functional Flow Block Diagram F.1--F.12 for the platform-wide flow, with OR/AND gates and a dashed feedback edge F.12 $\rightarrow$ F.1 closing the continuous-optimization loop (\S\ref{sec:cont-opt}). Block F.11 (points) is rendered with a red striped border to flag the production deployment gap (\texttt{point\_rules}\,$=$\,0 rows; \texttt{point\_transactions} table missing per Table~\ref{tab:deployment}).}
  \label{fig:mbse-ffbd}
\end{figure*}

\subsection{Carpool Module}\label{sec:carpool-overview}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_usecase_request_ride.pdf}
  \caption{Use Case Diagram for the carpool capability. Three actors (Rider, Activity Organizer, Driver), 10 use-case ovals coloured by priority, and \texttt{«include»} / \texttt{«extend»} connectors mark mandatory sub-flows and condition-gated extensions. Italic call-outs flag designed-but-uninstrumented use cases (rating, points, SOS) per the 2026-04-23 snapshot.}
  \label{fig:mbse-usecase}
\end{figure}

The carpool module supports three distance categories: in-Ithaca commuting, short-distance regional trips, and long-distance trips to metropolitan areas (e.g., New York City, Boston, Syracuse Hancock Airport). It engages all four design primitives. The driver supply-willingness data (\finding{6}: long-distance 12/33 Very or Extremely willing, the highest of the three scenarios at 36\%) directly motivated the design prioritization of long-distance trip matching as the primary use case.

\paragraph{State machine and booking flow.} A ride row in the \texttt{rides} table moves through four states: \texttt{active} $\rightarrow$ \texttt{full} (when bookings fill all seats) $\rightarrow$ \texttt{completed} (driver-triggered) or \texttt{cancelled} (driver-triggered, soft-delete). A booking row in \texttt{ride\_bookings} moves through \texttt{confirmed} (default, since we treat the demand-side as the decision point for this pilot) $\rightarrow$ \texttt{cancelled}. Seat availability is recomputed server-side on every booking and cancellation, rather than stored as a counter, so race conditions in the ``last seat'' case are narrow. Cancellation is disallowed after the scheduled \texttt{departure\_time}. A ride cannot be updated once its status is \texttt{completed} or \texttt{cancelled}, and only the \texttt{driver\_id} of a ride may trigger \texttt{completeRide}. These invariants are enforced at the controller layer, not via database constraints alone, so they are only as strong as the controller path.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_state_machine_unified.pdf}
  \caption{Combined UML State Machine for the three coupled entities of a carpool ride: \texttt{Ride} (\texttt{active}\,$\to$\,\texttt{full}\,$\to$\,\texttt{completed}\,$|$\,\texttt{cancelled}), \texttt{RideBooking} (\texttt{confirmed}\,$\to$\,\texttt{cancelled}), and \texttt{Group(group\_kind='ride\_carpool')} (\texttt{created}\,$\to$\,\texttt{active}\,$\to$\,\texttt{expired}). Within-entity transitions are drawn solid in trigger\,[guard]\,/\,effect form; the dashed cross-cluster edges are the four side-effect couplings: \texttt{bookRide()} may flip the Ride to \texttt{full} and may create the Group; \texttt{cancelBooking()} may unflag \texttt{full} and removes the corresponding \texttt{group\_members} row; \texttt{updateRide(departure\_time)} resets \texttt{Group.chat\_expires\_at}; \texttt{completeRide()} triggers no booking or group transition (the Group expires on its own \texttt{departure + 1h} timer).}
  \label{fig:mbse-state-unified}
\end{figure*}

\paragraph{Booking side-effects.} A single successful booking triggers three controller-level side-effects: (1)~an optional transition of the ride to \texttt{full} when the new booking exhausts the remaining seats; (2)~six notification records emitted via \texttt{notification.service.sendNotification}, spanning five categories---\texttt{ride\_new\_booking}, \texttt{ride\_booking\_confirmed}, \texttt{ride\_payment\_confirmed}, \texttt{ride\_payment\_received}, and two \texttt{ride\_rating\_reminder} rows (one per role) whose \texttt{data.showAfter} field is set to \texttt{departure\_time + 2h}---each of which also emits one Socket.IO event on the recipient's \texttt{user:\{recipient\_id\}} room as a bundled side-effect of the notification service's default \texttt{channels=['socket','database']} setting; and (3)~an idempotent \texttt{ride\_carpool} group chat ensure that creates the group on first booking and adds the driver and passenger to \texttt{group\_members} (detailed in \S\ref{sec:dd-messaging}). The WeChat outreach record (\texttt{wxgroup\_notice\_record}) often listed alongside booking is in fact written by \texttt{createRide} when a driver \emph{publishes} a ride, not by \texttt{bookRide}; the 16 ride-related rows in the 2026-04-23 snapshot (\S\ref{sec:deployment-feedback}) therefore correspond to historical ride publications, not to bookings. Figures~\ref{fig:mbse-swimlane} and~\ref{fig:mbse-seq} render the \texttt{bookRide()} flow as a Rider/System/Driver swimlane and as a UML sequence diagram with two \texttt{alt} fragments and one notification-fan-out \texttt{loop}; both visually mark the \texttt{wxgroup\_notice\_record} honesty correction. Detailed design decisions follow in \S\ref{sec:deep-dive}.

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_act_swimlane_book_ride.pdf}
  \caption{Activity-diagram swimlane (Rider $\mid$ System $\mid$ Driver) tracing \texttt{bookRide()} (\texttt{carpooling.controller.js:511-709}) line-for-line. Yellow diamonds are decisions; black bars are forks/joins for the parallel notification fan-out. The orange honesty note records that \texttt{wxgroup\_notice\_record} fires on \texttt{createRide}, not on \texttt{bookRide}.}
  \label{fig:mbse-swimlane}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_seq_book_ride.pdf}
  \caption{UML Sequence Diagram for \texttt{bookRide}. Six lifelines (Rider Browser, \texttt{carpoolingController.bookRide}, Supabase Postgres, NotificationService, Socket.IO Hub, faded WeChat Worker); two \texttt{alt} fragments (seats\,$=$\,0 $\rightarrow$ 409; last seat $\rightarrow$ \texttt{UPDATE rides SET status='full'}) and one \texttt{loop} fragment over the 6 notification types (each: \texttt{INSERT notifications} + \texttt{socket.emit} on \texttt{user:\{recipient\}}). Idempotent \texttt{INSERT}s into \texttt{groups}/\texttt{group\_members} silently swallow Postgres code 23505.}
  \label{fig:mbse-seq}
\end{figure*}

\subsection{Marketplace Module}\label{sec:marketplace}

The marketplace module enables peer-to-peer secondhand trading inside the \edudot{} scope. A listing in \texttt{marketplace\_items} carries \texttt{seller\_id}, \texttt{title}, \texttt{description}, \texttt{category}, \texttt{price}, \texttt{condition} (one of \texttt{new} / \texttt{like\_new} / \texttt{good} / \texttt{fair} / \texttt{poor}), \texttt{location}, a \texttt{text[]} of \texttt{images}, a \texttt{text[]} of \texttt{tags}, a life-cycle \texttt{status} (\texttt{active} / \texttt{sold} / \texttt{removed}), and aggregate counters \texttt{views\_count} and \texttt{favorites\_count}. Social surface comes from three companion tables: \texttt{marketplace\_comments} (threaded comments with soft-delete), \texttt{marketplace\_comment\_likes}, and \texttt{item\_favorites}. Deletion is implemented as a \texttt{status = 'removed'} soft-delete rather than row deletion, so a seller who retracts a listing leaves an auditable trail for the rating system and for cross-user conversation threads.

\paragraph{Cross-module reuse.} Marketplace reuses three of the four carpool primitives. Identity: the \edudot{} JWT is the shared admission gate, and the seller card on every listing carries the same verified-Cornell badge that drivers do. Messaging: clicking ``Contact seller'' opens a direct-message thread whose \texttt{context\_type = 'marketplace'} and \texttt{context\_id = <item\_id>}, letting the recipient's inbox group messages by listing. Rewards: a successful transaction writes a \texttt{marketplace\_transaction} point-transaction (base 8 points per the application-code catalog, Table~\ref{tab:pointrules}), though in production this path has not yet written transactions. \emph{Safety primitives are deferred to future work}: the present marketplace module does not implement an in-person meet-up safety layer (no SOS, no real-time location share, no escrowed exchange), and the only safety-adjacent affordances are the inherited \edudot{} gate and the \texttt{REPLY\_REQUIRED} cold-DM guard (\S\ref{sec:messages}); a dedicated marketplace safety design is part of the roadmap.

\paragraph{Outreach path.} Every newly created listing fires a \texttt{wxgroup\_notice\_record} insert formatted as ``二手上新 $\langle$title$\rangle$ + short link,'' where the link is resolved by \texttt{wechatLinkService.getBestNoticeLink}---mini-program short link if available, H5 URL as fallback. In the 2026-04-23 snapshot this path accounts for 62 of 82 \texttt{wxgroup\_notice\_record} rows, making the marketplace the single largest producer of outbound WeChat pushes. The live 15-item inventory, all \texttt{status = 'removed'} with 12 aggregate views and 0 favorites (\S\ref{sec:deployment-feedback}), shows the ingestion and cross-posting path works end-to-end even though organic buyer uptake has not yet followed.

\subsection{Activities Module}\label{sec:activities}

The activities module supports event publication, registration, geo-verified check-in, and post-event rating. An \texttt{activities} row specifies a \texttt{category} chosen from \{\texttt{academic}, \texttt{sports}, \texttt{social}, \texttt{volunteer}, \texttt{career}, \texttt{cultural}, \texttt{technology}\}, a \texttt{type} from \{\texttt{individual}, \texttt{team}, \texttt{competition}, \texttt{workshop}, \texttt{seminar}\}, a \texttt{location} string paired with a \texttt{location\_coordinates} JSONB, time bounds (\texttt{start\_time}, \texttt{end\_time}, \texttt{registration\_deadline}), capacity (\texttt{max\_participants}, \texttt{current\_participants}), pricing (\texttt{entry\_fee} cash, \texttt{entry\_fee\_points} cross-module pay-with-points), reward metadata (\texttt{reward\_points}), a six-digit \texttt{checkin\_code}, boolean \texttt{location\_verification}, and a status machine \{\texttt{draft}, \texttt{published}, \texttt{ongoing}, \texttt{completed}, \texttt{cancelled}\}. A companion \texttt{activity\_participants} row tracks each registration with \texttt{attendance\_status} (\texttt{registered} / \texttt{attended} / \texttt{cancelled} / \texttt{no\_show}), \texttt{payment\_status} (\texttt{pending} / \texttt{paid} / \texttt{refunded}), \texttt{points\_earned}, and a 1--5 \texttt{rating} field that the organizer populates on completion.

\paragraph{Counter consistency.} \texttt{current\_participants} is maintained by the \texttt{update\_activity\_participant\_count} PL/pgSQL trigger, which increments on \texttt{INSERT} of a \texttt{registered} row and decrements when the \texttt{attendance\_status} transitions out of \texttt{registered}, so the displayed seat count cannot diverge from the registration rows.

\paragraph{Geo-verified check-in.} The check-in window opens \texttt{checkin\_start\_offset} minutes (default 30) before \texttt{start\_time} and closes \texttt{checkin\_end\_offset} minutes (default 30) after \texttt{end\_time}; the \texttt{is\_checkin\_period} Postgres function enforces this. Inside the window, a participant submits a location JSONB (\texttt{\{latitude, longitude, accuracy\}}); the \texttt{calculate\_distance} function computes Haversine distance to \texttt{activity.location\_coordinates} and marks \texttt{location\_verified = true} if it falls within \texttt{verification\_radius} (default 100\,m). The full check-in row in \texttt{activity\_checkins} additionally captures \texttt{device\_info} JSONB (browser user-agent) and \texttt{ip\_address}, so spoof attempts leave a forensic trail. A successful, geo-verified check-in is the trigger for the \texttt{activity\_checkin} point-rule (5 points in the application-code catalog).

\paragraph{Cross-module reuse.} Identity reuses the \edudot{} JWT; messaging is embedded per-activity through \texttt{activity\_chat\_messages} and via DM threads scoped with \texttt{context\_type = 'activity'}; rewards flow both directions (reward on completion, optional spend via \texttt{entry\_fee\_points}); the ride-style social channel is reused via automatic \texttt{wxgroup\_notice\_record} pushes on publication. In the 2026-04-23 snapshot the \texttt{activities}, \texttt{activity\_participants}, \texttt{activity\_checkins}, and \texttt{activity\_chat\_messages} tables all hold zero rows, but 4 \texttt{wxgroup\_notice\_record} activity pushes and 4 \texttt{activity\_registered} / 4 \texttt{activity\_new\_registration} notifications (\S\ref{sec:deployment-feedback}) attest to a short run of activity events in February 2026 whose transactional rows have since been cleaned.

\subsection{Groups Module}\label{sec:groups}

The groups module provides two kinds of persistent social containers sharing one table. A \texttt{groups} row carries \texttt{name}, \texttt{description}, \texttt{cover\_image}, \texttt{creator\_id}, \texttt{member\_count}, and a \texttt{group\_kind} discriminator whose two current values are \texttt{community} (interest- or geography-based groups) and \texttt{ride\_carpool} (trip-bound groups, \S\ref{sec:dd-messaging}); ride-bound rows additionally set \texttt{ride\_id} and \texttt{chat\_expires\_at}. Membership lives in \texttt{group\_members} with a \texttt{role} of \texttt{creator} or \texttt{member}.

\paragraph{Messaging substrate.} \texttt{group\_messages} enforces a \texttt{char\_length(content) BETWEEN 1 AND 2000} check, a \texttt{message\_type} enum of \{\texttt{text}, \texttt{image}, \texttt{file}\}, and a soft-delete column (\texttt{deleted\_at}) so moderation actions do not rewrite history. Row-level security is non-trivial here: the \texttt{group\_messages\_select\_policy} admits \texttt{SELECT} only to rows whose \texttt{auth.uid()} has a live \texttt{group\_members} entry, and the insert policy additionally forces \texttt{auth.uid() = sender\_id}, so the identity claim on every message is structurally rather than application-enforced. Update and delete policies are restricted to the original sender, and a server-side trigger keeps \texttt{updated\_at} fresh.

\paragraph{Moderation (migration~010).} A group creator or a platform moderator can mute a member through \texttt{group\_muted\_users} (\texttt{muted\_by}, optional \texttt{reason}, \texttt{muted\_at}, \texttt{unmuted\_at}) and can retract a message through \texttt{group\_message\_deletions} (which pairs with the soft-delete fields \texttt{is\_deleted}, \texttt{deleted\_at}, \texttt{deleted\_by} on \texttt{group\_messages}). These affordances exist for community groups but, as \S\ref{sec:dd-messaging} notes, are not yet wired into the ride-scoped \texttt{ride\_carpool} rooms.

\paragraph{System groups and discovery.} Migration~008 provisions two system-level rooms with fixed UUIDs---a platform-wide Carpooling room (\texttt{00000000-0000-0000-0000-000000000001}) and a Marketplace room (\texttt{...002})---that all users can reach without joining. A group-map view atop \texttt{cover\_image} + optional geography furnishes the social-discovery layer. In the 2026-04-23 snapshot, \texttt{groups} holds 5 \texttt{community} rows, all with \texttt{member\_count = 1} (creator-only), suggesting that group creation is working but that the discovery-to-join funnel has not yet had its flywheel moment.

\subsection{Messages Module}\label{sec:messages}

The messaging module carries three distinct surfaces on a shared Socket.IO substrate: direct messages (\texttt{messages}), group chat (\texttt{group\_messages}, \S\ref{sec:groups}), and system messages (\texttt{system\_messages}, including a user-submitted-feedback channel).

\paragraph{Direct-message schema.} A \texttt{messages} row records \texttt{sender\_id}, \texttt{receiver\_id}, \texttt{subject} (2--255 chars), \texttt{content} (1--2000 chars), and four typing dimensions: \texttt{message\_type} (\texttt{general} / \texttt{activity\_inquiry} / \texttt{activity\_update} / \texttt{support}), \texttt{context\_type} and \texttt{context\_id} which cross-link a message to its originating object (a ride, a listing, an activity), \texttt{priority} (\texttt{low} / \texttt{normal} / \texttt{high}), and \texttt{thread\_id} plus \texttt{reply\_to} for threading. The companion \texttt{message\_participants} row represents each side's view (read status, archive flag) so that one user's archival does not mutate the counterparty's inbox.

\paragraph{Reply-required guard against cold-message spam.} The \texttt{messageService.sendMessage} path enforces a \texttt{REPLY\_REQUIRED} rule: once a user has sent a direct message to a recipient they have no prior thread with, subsequent messages are refused with HTTP~403 until the recipient replies at least once. This is a platform-side mitigation for unsolicited mass DMs; it is a light-touch analog of the first-message-friction pattern often discussed in sharing-economy safety literature.

\paragraph{System messages and the feedback channel.} \texttt{system\_messages} carries a \texttt{sender\_type} of \texttt{admin} (pinned announcements) or \texttt{user} (submitted feedback). Each row optionally pins (\texttt{is\_pinned}) and typologizes via \texttt{message\_type}. In the 2026-04-23 snapshot all 10 rows have \texttt{sender\_type = 'user'} and \texttt{message\_type = 'feedback'}, dated 2026-01-10 to 2026-02-11; no admin announcements have been posted yet, meaning the user-feedback subsurface is, in practice, the entire current use of the system-messages surface.

\paragraph{Real-time substrate.} Socket.IO rooms namespace three kinds of live state: \texttt{user:\{userId\}} for personal notifications and presence, \texttt{activity:\{activityId\}} for activity chat, and \texttt{thread:\{threadId\}} for DM and group-message typing indicators. JWT authentication on connect is mandatory; guests receive a limited \texttt{type='guest'} token. The \texttt{typing\_indicator} event is broadcast to the thread room excluding the sender, matching the UX idiom users expect from WeChat.

\paragraph{Cross-module embedding.} Messaging is deeply embedded with every other module: a carpool booking materializes a \texttt{ride\_carpool} group (\S\ref{sec:dd-messaging}); a marketplace ``Contact seller'' opens a \texttt{context\_type='marketplace'} DM; activities carry both a group chat and DM threads with \texttt{context\_type='activity'}. This embedding is what the Introduction means by ``multi-module''---the modules are not simply co-installed apps but share the same conversational substrate. Live data (\S\ref{sec:deployment-feedback}): 22 DMs, all \texttt{message\_type='general'} and all \texttt{is\_read=true}, concentrated in a 3-week burst around 2026-02-05 to 2026-02-28; plus 18 \texttt{message\_reply} notifications attesting to that burst.

\subsection{Points Module (Cross-Module Gamification)}\label{sec:points-overview}

The points module is a cross-module meta-layer that treats every other module as both a \emph{source} and a \emph{sink} of points. Sources: registration, email verification, profile completion, daily login, ride creation and completion, marketplace transaction, activity creation / organization / participation / check-in / completion, and a consecutive-check-in streak bonus (the only rule that honors the \texttt{multiplier} field). Sinks: a \texttt{coupons} table (currently empty) for redemption rewards, and the \texttt{activities.entry\_fee\_points} field, which lets an organizer charge an activity in points rather than cash. A single \texttt{awardPoints} service writes a row to \texttt{point\_transactions} with \texttt{rule\_type}, \texttt{source}, \texttt{reason}, \texttt{metadata}, and \texttt{multiplier}, and atomically increments \texttt{users.points} via the \texttt{increment\_user\_points} RPC; a symmetric \texttt{deductPoints} refuses to go below zero. Design rationale and the full rule catalog are in \S\ref{sec:dd-gamification}.

\paragraph{Why secondary by design.} The motivation data (\finding{4}: gamification at 48.3, the second tier behind financial motivation at 63.6) informed a deliberate design choice: base-point payouts are capped well below the cash value of the corresponding transaction (e.g., 15 points for a completed ride whose per-seat price is typically \$22--\$38), so points complement rather than substitute the cash lever. This avoids the algorithmic-management failure mode where a gamified point economy becomes the dominant motivator and then warps participation into point-chasing (\S\ref{sec:discussion-limits}).

\paragraph{Deployment status caveat.} The points subsystem is present in code but \emph{not yet provisioned in the Railway-backed production database}: \texttt{point\_rules} has zero rows, \texttt{point\_transactions} does not exist as a table, and every one of the 184 live user rows carries \texttt{users.points = 0}. The design is therefore implementation-ready but behaviorally inert; we flag this in \S\ref{sec:dd-gamification} and \S\ref{sec:deployment-feedback} rather than paper over it.

\subsection{Carpool Deep-Dive: Five Design Decisions}\label{sec:deep-dive}

Each design decision below is explicitly motivated by a survey finding, and each is described against the implemented controller / service / schema that backs it in the deployed system (\S\ref{sec:deployment-feedback}). Decisions 1--4 correspond to the four design primitives distilled in \S\ref{sec:rw-primitives}; decision 5 documents the cross-module integration lever that makes the multi-module claim operational at the ride level. Figure~\ref{fig:mbse-ride-lifecycle} renders the full ride lifecycle from \texttt{createRide} through \texttt{completeRide} as an activity diagram in which solid green nodes mark deployed-and-exercised paths and dashed-grey nodes mark designed-but-uninstrumented elements (rating submission, SOS fan-out, points award) per the 2026-04-23 production snapshot.

\begin{figure}[t]\centering
  \includegraphics[width=0.85\linewidth]{pic/mbse_act_full_ride_lifecycle.pdf}
  \caption{Full ride lifecycle activity diagram from \texttt{createRide} $\rightarrow$ \texttt{bookRide} $\rightarrow$ 2\,h delay $\rightarrow$ \texttt{completeRide}. Solid green nodes are deployed and exercised in the 2026-04-23 snapshot; dashed-grey nodes are designed-but-uninstrumented (rating submission with \texttt{ratings} at 0 rows, SOS fan-out with 0 invocations, points award with \texttt{point\_rules} unmigrated). Decision diamonds: seats $> 0$, rating window open, SOS triggered.}
  \label{fig:mbse-ride-lifecycle}
\end{figure}

\subsubsection{Identity Verification}\label{sec:dd-identity}

\emph{Design decision}: \edudot{} email verification as a registration gate and a persistent trust signal displayed on driver and passenger profiles.

\emph{Evidence}: \finding{3} shows \edudot{} verification has a mean WTP uplift of 67.3 (median 79), the second-highest of the seven safety features.

\emph{Implementation}: New users supply an \texttt{email}, \texttt{password}, \texttt{first\_name}, \texttt{last\_name}, and \texttt{student\_id}; the backend generates an \texttt{email\_verification\_token} (and \texttt{email\_verification\_expires}) and sends a verification mail via Resend. Clicking the link flips the row's \texttt{is\_verified} flag to \texttt{true}. A second, stricter flag, \texttt{verification\_status} (values \texttt{pending} / \texttt{verified}), is reserved for future manual-review workflows but currently transitions in lockstep with \texttt{is\_verified} because the manual-review step is not yet instantiated. The Socket.IO authentication middleware accepts only a JWT signed with the Cornell-scoped user row; guests receive a separate \texttt{type='guest'} token with read-only capabilities. The verified badge and \texttt{university} string (``Cornell University'') are embedded in every driver and passenger card returned by \texttt{getRides} and \texttt{getRideById}.

\emph{Limitation}: \edudot{} verification confirms institutional affiliation but does not verify driving competence, behavioral reliability, or insurance status. The pilot observation on the Railway-backed production database (\S\ref{sec:deployment-feedback}) shows 170 of 184 user rows with \texttt{is\_verified = true} and an identical count in \texttt{verification\_status = 'verified'}, confirming that the \edudot{} token loop is self-consistent and that 100\% of rows carry a \texttt{@cornell.edu} address, but also that the two-tier model collapses to a one-tier gate in practice because no manual-review queue is running.

\subsubsection{Safety Skeleton}\label{sec:dd-safety}

\emph{Design decision}: Real-time location sharing and a one-tap SOS button as two active safety layers during trips.

\emph{Evidence}: \finding{3} shows real-time location sharing as the highest-WTP feature (mean 69.1, median 76) and Emergency SOS as the third-highest (mean 63.5, median 64).

\emph{Implementation}: Each ride booking admits its driver and passenger to a Socket.IO room namespaced as \texttt{thread:\{thread\_id\}} and, in parallel, to the auto-created ride-scoped group chat room (\S\ref{sec:dd-messaging}). Typing indicators, online presence, and position updates are broadcast inside these rooms only. The SOS button triggers a high-priority \texttt{notification} row with \texttt{priority = 'high'} targeted at pre-configured emergency contacts and the current passenger set, plus an immediate Socket.IO emit on each recipient's \texttt{user:\{userId\}} room; device context (browser user-agent, IP, geolocation accuracy) is captured in the activity check-in schema's \texttt{device\_info} JSONB column and is reused for the rideshare SOS path. Activities that opt in to location-gated check-in compute Haversine distance between the user location JSONB (\texttt{\{latitude, longitude, accuracy\}}) and the activity's coordinates using the \texttt{calculate\_distance} Postgres function, with a configurable \texttt{verification\_radius} (default 100\,m); the same primitive is available to the rideshare module for pickup-point verification.

\emph{Limitation}: Location sharing creates a privacy trade-off that the current implementation resolves by room-scoping rather than by retention policy---raw coordinates are not persisted beyond the active session but also are not redacted in ride-group chat messages. SOS response chains depend on resources outside the platform, and the pilot has recorded zero SOS activations, so the end-to-end latency of the SOS path is currently uninstrumented.

\subsubsection{Rating System with Fairness Consideration}\label{sec:dd-rating}

\emph{Design decision}: Bidirectional (passenger $\leftrightarrow$ driver) ratings on a 1--5 integer scale with optional free-text comments; a deferred rating-readiness window that opens 2\,hours after \texttt{departure\_time} (or at \texttt{status = 'completed'}) rather than at booking; role-paired rating so that only the trip's driver may rate its passengers and vice versa; and self-revision of one's own rating via update-in-place until subsequent system-level mechanisms retire the row.

\emph{Evidence}: \finding{5}, limited to the Driver/Both subset ($N{=}19$): ``unfair rating'' tolerance at 29.1 is 12.3--23.2 points below the other three items (41.4--52.3), indicating that rating-system fairness is the most salient concern for respondents with driving experience.

\emph{Implementation}: The \texttt{ratings} table keys on \texttt{(trip\_id, rater\_id, ratee\_id)} and records \texttt{role\_of\_rater} (\texttt{'driver'} or \texttt{'passenger'}), \texttt{score} (CHECK 1--5), \texttt{comment}, and timestamps. The \texttt{createRating} controller refuses self-ratings, verifies that the rater is either the ride's driver or a non-cancelled passenger via a \texttt{ride\_bookings} lookup, enforces that drivers may only rate their passengers (and vice versa), and blocks submission until \texttt{Date.now() >= departure\_time + 2h} (constant \texttt{RATING\_READY\_DELAY\_MS}). An existing rating row is overwritten rather than appended, and the user-level \texttt{users.avg\_rating} / \texttt{users.total\_ratings} cache is recomputed as an unweighted mean across the union of \texttt{ratings} and \texttt{activity\_ratings} rows for the ratee. A pair of \texttt{ride\_rating\_reminder} notifications with \texttt{data.showAfter = departure + 2h} is queued at booking time so both sides see a tap-to-rate card in their message inbox once the window opens.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_param_rating_window.pdf}
  \caption{SysML Parametric Diagram for the rating-window guard in \texttt{rating.controller.js::createRating}. Three \texttt{«constraint»} blocks chain in order: \texttt{NotSelfRating} ($\textit{is\_valid}\,\equiv\,\textit{rater\_id}\,\ne\,\textit{ratee\_id}$), \texttt{RoleEligible} (driver--passenger pairing on the trip's \texttt{rides} row), and \texttt{RatingWindowOpen} ($\textit{is\_open}\,\equiv\,(\textit{now}\,-\,\textit{departure\_time})\,\ge\,\textit{delay}$, with delay\,$=$\,\texttt{RATING\_READY\_DELAY\_MS}\,$=$\,2\,h\,$=$\,7{,}200{,}000\,ms). Value properties drawn as small rectangles bind to the constraints via solid connectors with no arrowheads (UML convention). The chained constraint outputs feed a Pass\,/\,Reject decision; in the 2026-04-23 snapshot the \texttt{ratings} table holds zero rows so this guard chain has been exercised zero times in production.}
  \label{fig:mbse-param-rating}
\end{figure*}

\emph{Design rationale}: Field experiments on two-sided reputation systems~\citep{Fradkin2021} show that architectural choices (e.g., hiding feedback until both parties submit) change rating behavior. The 2-hour readiness delay is a simpler variant of this architectural idea: it removes the in-vehicle moment from the rating submission path, reducing the most immediate retaliation surface. The role-pairing and self-revision primitives draw on CSCW design-case work on algorithm-based reputation systems for peer-to-peer carsharing~\citep{Neifer2023}.

\emph{Scope of the implemented design}: Three mechanisms that we considered---a formal pre-publication dispute window, cross-trip trend protection for a single anomalous rating, and mandatory rating justifications---are \emph{not} yet implemented. Update-in-place is the only present-day revision affordance and does not bind either party to a fixed deliberation period. We retain the other three as open design proposals; their absence in the live system is part of the honest audit trail (\S\ref{sec:pipeline-audit}). The $N{=}19$ subset also limits the empirical basis for the rating-fairness decision more broadly.

\emph{Limitation}: Update-in-place allows a disgruntled rater to revise downward at any time, which is the opposite failure mode from the dispute-window design. Simple-mean aggregation provides no outlier smoothing, so the first negative rating dominates the displayed \texttt{avg\_rating} for a new driver. And because \texttt{ratings} currently contains zero rows in the live database (\S\ref{sec:deployment-feedback}), whether any of these mechanisms alleviate driver rating anxiety cannot be assessed without sustained usage.

\subsubsection{Gamification as Secondary Incentive}\label{sec:dd-gamification}

\emph{Design decision}: Points serve as a secondary incentive layer, deliberately not dominating the economic motivation.

\emph{Evidence}: \finding{4} places gamification (48.3) in a second tier behind financial motivation (63.6).

\emph{Implementation}: All point-affecting events route through a single \texttt{awardPoints} service that writes a row to \texttt{point\_transactions} (\texttt{user\_id}, \texttt{rule\_type}, \texttt{points}, \texttt{source}, \texttt{reason}, \texttt{metadata}, \texttt{multiplier}, \texttt{created\_at}) and atomically increments \texttt{users.points} via the \texttt{increment\_user\_points} RPC. The application-code rule catalog (Table~\ref{tab:pointrules}) sets \texttt{registration = 10}, \texttt{verification = 5}, \texttt{daily\_login = 1}, \texttt{profile\_complete = 15}, and a set of activity-triggered rewards (\texttt{activity\_creation = 15}, \texttt{activity\_participation = 10}, \texttt{activity\_organization = 30}, \texttt{activity\_checkin = 5}, \texttt{activity\_completion = 15}); the \texttt{points.service} additionally defines \texttt{rideshare\_completion = 15}, \texttt{marketplace\_transaction = 8}, \texttt{referral = 30}, and a \texttt{consecutive\_checkin} streak rule whose \texttt{multiplier} attribute is respected by \texttt{awardPoints}. A \texttt{deductPoints} counterpart refuses to go below zero (returning \texttt{INSUFFICIENT\_POINTS}) so points are kept non-negative. The base-point schedule is deliberately capped below the per-seat cash price of a typical long-distance ride, so points remain a complement to, not a substitute for, cash.

\begin{table}[ht]
  \centering
  \caption{Points rule catalog as defined in application code (\texttt{points.service} and activity migration seed). In the Railway-backed production database, \texttt{point\_rules} currently holds zero rows and \texttt{point\_transactions} has not been migrated---see \S\ref{sec:deployment-feedback}.}\label{tab:pointrules}
  \smallskip
  \begin{tabular}{@{} l l r l @{}}
    \toprule
    Rule & Category & Base & Notes \\
    \midrule
    \texttt{registration}           & system  & 10 & One-shot on \texttt{users} insert \\
    \texttt{verification}           & system  &  5 & On \texttt{is\_verified} flip \\
    \texttt{daily\_login}           & system  &  1 & Idempotent per calendar day \\
    \texttt{profile\_complete}      & system  & 15 & On avatar / major populated \\
    \texttt{activity\_creation}     & social  & 15 & On \texttt{activities} insert \\
    \texttt{activity\_participation}& social  & 10 & On \texttt{activity\_participants} insert \\
    \texttt{activity\_organization} & social  & 30 & Organizer bonus at completion \\
    \texttt{activity\_checkin}      & social  &  5 & On geo-verified \texttt{activity\_checkins} \\
    \texttt{activity\_completion}   & social  & 15 & On \texttt{status = 'completed'} \\
    \bottomrule
  \end{tabular}
\end{table}

\emph{Limitation}: Cross-module points may incentivize gaming behavior such as fake trips, collusive check-ins, or strategic compliance; the only present anti-gaming lever is the \texttt{validateActivityPoints} stub, which returns \texttt{\{valid: true\}} and is explicitly annotated as a placeholder for future rate-limit logic. No deduplication at the \texttt{(user, rule, day)} level is enforced at the database layer. More fundamentally, the entire points subsystem is \emph{not yet deployed}: the Railway-backed production database holds zero rows in \texttt{point\_rules} and lacks the \texttt{point\_transactions} table altogether (the REST API returns \texttt{PGRST205} when queried), and every one of the 184 live user rows has \texttt{users.points = 0}. The gamification design described here therefore reflects implementation readiness at the controller / service layer rather than an observed behavioral lever in the current soft launch (\S\ref{sec:deployment-feedback}). The absence of production \texttt{point\_transactions} also means the hypothesis that financial motivation dominates gamification (\finding{4}) is neither challenged nor corroborated by current usage data.

\subsubsection{Messaging Embedding: Ride-Scoped Group Chat}\label{sec:dd-messaging}

\emph{Design decision}: Every carpool booking materializes a ride-scoped group chat, so communication follows the trip rather than the individuals. The chat is automatically created on first booking, auto-expires one hour after the scheduled departure, and tracks membership against live bookings.

\emph{Evidence}: The grassroots-practice literature we review in \S\ref{sec:rw-grassroots} documents that students already run ride coordination inside persistent WeChat / WhatsApp groups~\citep{Liu2023, Bonini2023}. Our survey observation that 17 of 21 Mandarin-native respondents who answered the carpool-finding question used such groups resonates with that pattern.

\emph{Implementation}: The \texttt{ensureRideCarpoolGroupOnBooking} service, called inline from \texttt{bookRide}, looks up any existing \texttt{groups} row with the booking's \texttt{ride\_id}. If none exists, it inserts one with \texttt{group\_kind = 'ride\_carpool'}, \texttt{name = `Ride: <title>'}, \texttt{creator\_id = driver\_id}, and \texttt{chat\_expires\_at = departure\_time + 1h}. The driver is inserted into \texttt{group\_members} with \texttt{role = 'creator'} and the passenger with \texttt{role = 'member'} (duplicate-key collisions on Postgres code \texttt{23505} are silently swallowed to make the call idempotent). On passenger cancellation, \texttt{removePassengerFromRideGroup} deletes their \texttt{group\_members} row while leaving the group intact for remaining riders. A subsequent \texttt{updateRide} that changes \texttt{departure\_time} calls \texttt{syncRideCarpoolGroupExpiry}, which re-computes and writes \texttt{chat\_expires\_at}. Messages inside these rooms flow through the same Socket.IO thread-room primitive as direct messages, so the typing indicator and read-receipt affordances are shared across module boundaries. Row-level security on \texttt{group\_messages} restricts \texttt{SELECT} to current group members and \texttt{INSERT} to current members posting as themselves.

\emph{Limitation}: The one-hour post-departure expiry matches the ``trip-bound'' framing of the module but forecloses post-trip reconciliation chat (for lost items, fare corrections, or trailing rating disputes) unless one party re-opens the thread as a direct message. Ride-scoped chats do not inherit mute or moderation state from the system-level moderation tables added for community groups in migration~010, so a misbehaving co-rider cannot be muted inside the ride chat without kicking them. In the Railway-backed production database no \texttt{group\_kind = 'ride\_carpool'} rows are currently live (all five extant groups are \texttt{community}); the 82 ride-related push records in \texttt{wxgroup\_notice\_record} and the 8 queued \texttt{ride\_rating\_reminder} notifications attest to historical ride bookings that pre-date the current \texttt{rides} table state (\S\ref{sec:deployment-feedback}).

\subsection{Soft-Launch Deployment Feedback}\label{sec:deployment-feedback}

\campusride{} has been continuously reachable at \texttt{www.campusgo.college} since 2026-01-08, backed by a Railway-hosted Node.js backend and a Supabase Postgres instance (project reference \texttt{bwimyvkwkenrtumsfjzt}). This section reports a 2026-04-23 snapshot of that production database as implementation-status evidence; Table~\ref{tab:deployment} summarizes per-table row counts along with notification-attested historical activity. We frame these numbers as formative deployment signal, not as an evaluation: the sample is opportunity-recruited from the authors' Cornell network via WeChat-group outreach (82 \texttt{wxgroup\_notice\_record} pushes across the pilot window), user-generated ride / activity / points activity has been limited, and no experimental comparison is in place.

\begin{table}[ht]
  \centering
  \caption{Live production database snapshot, 2026-04-23 (Supabase project \texttt{bwimyvkwkenrtumsfjzt}). Pilot window: 2026-01-08 to 2026-03-29 for user registrations.}\label{tab:deployment}
  \smallskip
  \begin{tabular}{@{} l r l @{}}
    \toprule
    Table / surface & Rows & Notes \\
    \midrule
    \texttt{users}                     & 184 & 184 \texttt{@cornell.edu} (100\%); 170 verified \\
    \texttt{rides}                     &   0 & no currently active rides \\
    \texttt{ride\_bookings}            &   0 & empty; historical bookings evidenced in notifications \\
    \texttt{ratings}                   &   0 & no ratings submitted \\
    \texttt{activities}                &   0 & \\
    \texttt{activity\_participants}    &   0 & \\
    \texttt{marketplace\_items}        &  15 & all \texttt{status = 'removed'}; 12 aggregate views \\
    \texttt{marketplace\_comments}     &   0 & \\
    \texttt{groups}                    &   5 & all \texttt{group\_kind = 'community'}, 1 member each \\
    \texttt{group\_members}            &  10 & \\
    \texttt{group\_messages}           &   2 & \\
    \texttt{messages} (DM)             &  22 & all \texttt{read = true}, 8 \texttt{message\_participants} \\
    \texttt{notifications}             &  54 & 0 read; see Table~\ref{tab:notifs} for type mix \\
    \texttt{system\_messages}          &  10 & all user-submitted feedback (\texttt{message\_type = 'feedback'}) \\
    \texttt{point\_rules}              &   0 & \emph{catalog not migrated} \\
    \texttt{point\_transactions}       & --- & \emph{table does not exist} (REST \texttt{PGRST205}) \\
    \texttt{wxgroup\_notice\_record}   &  82 & 62 marketplace / 16 ride / 4 activity WeChat pushes \\
    \bottomrule
  \end{tabular}
\end{table}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_deployment_diagram.pdf}
  \caption{UML Deployment Diagram for \campusride{} v4.4. Three primary \texttt{«device»} nodes (Browser / Mobile, Railway Container, Supabase Cluster) host \texttt{«execution environment»} and \texttt{«artifact»} elements (Vue\,3 + Vite SPA / \texttt{bundle.js}; Node.js\,18 + Express running 23 controllers + 19 services + Socket.IO server; Postgres + RLS with 18 core tables, RLS policies, and the \texttt{increment\_user\_points} / \texttt{calculate\_distance} / \texttt{is\_checkin\_period} RPC functions). Three sidecar \texttt{«device»} nodes (Resend SMTP, WeChat Mini-Program API, TCAT bus schedule API) connect via labelled \texttt{«communication path»} edges (HTTPS REST + WebSocket; Postgres wire / RLS; SMTP via Resend; HTTPS to \texttt{wechatLinkService}). Snapshot 2026-04-23: 184 users, 82 \texttt{wxgroup\_notice\_record} rows, served at \texttt{www.campusgo.college}.}
  \label{fig:mbse-deployment}
\end{figure*}

\begin{table}[ht]
  \centering
  \caption{Notification type distribution in production (54 rows total). Each booking is designed to emit a 5-notification bundle plus 2 scheduled rating reminders; the row counts below are consistent with 4 historical bookings and 2 completed rides whose \texttt{rides} / \texttt{ride\_bookings} entries have since been cleaned.}\label{tab:notifs}
  \smallskip
  \begin{tabular}{@{} l r l @{}}
    \toprule
    Notification type & Rows & First $\rightarrow$ last \\
    \midrule
    \texttt{ride\_new\_booking}         & 4 & 2026-02-26 $\rightarrow$ 2026-04-01 \\
    \texttt{ride\_booking\_confirmed}   & 4 & 2026-02-26 $\rightarrow$ 2026-04-01 \\
    \texttt{ride\_payment\_received}    & 3 & 2026-03-08 $\rightarrow$ 2026-04-01 \\
    \texttt{ride\_payment\_confirmed}   & 3 & 2026-03-08 $\rightarrow$ 2026-04-01 \\
    \texttt{ride\_rating\_reminder}     & 8 & 2026-02-26 $\rightarrow$ 2026-04-01 \\
    \texttt{ride\_completed}            & 2 & 2026-02-26 $\rightarrow$ 2026-03-28 \\
    \texttt{activity\_new\_registration}& 4 & 2026-02-05 $\rightarrow$ 2026-02-22 \\
    \texttt{activity\_registered}       & 4 & 2026-02-05 $\rightarrow$ 2026-02-22 \\
    \texttt{message\_reply}             & 18 & 2026-02-06 $\rightarrow$ 2026-02-11 \\
    \texttt{new\_message}               & 4 & 2026-02-05 $\rightarrow$ 2026-02-28 \\
    \bottomrule
  \end{tabular}
\end{table}

\paragraph{What the snapshot suggests.} First, the \edudot{} gate is fully operational at scale: all 184 registered rows carry a \texttt{@cornell.edu} address, and 170 (92.4\%) have both \texttt{is\_verified} and \texttt{verification\_status} set to \texttt{verified}. Registration cadence grew monthly (3 in Jan, 70 in Feb, 111 in March), suggesting WeChat-group-driven acquisition is reaching the intended Cornell-affiliated audience. Second, the design's booking-to-notification fan-out (\S\ref{sec:carpool-overview}) is legible in the notification table: 4 \texttt{ride\_new\_booking} / \texttt{ride\_booking\_confirmed}, 3 \texttt{ride\_payment\_*} pairs, and 8 \texttt{ride\_rating\_reminder} rows match the expected 5+2 bundle for 4 historical bookings, providing residual evidence of ride transactions even though the \texttt{rides} and \texttt{ride\_bookings} tables currently hold zero rows (e.g., operator-side cleanup or the switchover to a different ride model). Third, the \texttt{wxgroup\_notice\_record} table (82 rows, Jan 17 -- Apr 11; 62 marketplace / 16 rideshare / 4 activity) shows that the WeChat cross-posting path runs automatically on every new ride, listing, or activity; this is the primary grassroots-to-platform bridge implied by the literature in \S\ref{sec:rw-grassroots}.

\paragraph{What the snapshot does not support.} The \texttt{ratings} table is empty, so the rating-system design of \S\ref{sec:dd-rating} remains implementation-complete but behaviorally unexercised in production. The \texttt{activities}, \texttt{activity\_participants}, \texttt{activity\_chat\_messages}, and \texttt{activity\_comments} tables are all at zero rows, and the 4+4 activity-notification pair in Table~\ref{tab:notifs} is the only trace of any activity run. The gamification subsystem is not deployed at all: \texttt{point\_rules} has zero rows, \texttt{point\_transactions} does not exist as a table, and \emph{every} one of the 184 user rows has \texttt{users.points = 0}. Marketplace usage, while larger than ride usage, is past-tense: all 15 items are \texttt{status = 'removed'} with 12 aggregate views and 0 favorites. The five live community groups each contain only their creator (\texttt{member\_count = 1}), so the group-discovery lever from \S\ref{sec:rw-grassroots} has not been exercised by joining behavior. And no \texttt{group\_kind = 'ride\_carpool'} rows exist at snapshot time, meaning the ride-scoped group-chat mechanism (\S\ref{sec:dd-messaging}) is evidenced indirectly (via 8 rating-reminder rows and 16 WeChat ride pushes) rather than directly in the \texttt{groups} table.

\paragraph{Implications for the claims in this paper.} The snapshot is consistent with the three contributions as stated: (1)~a \emph{design case} of an identity-verified six-module platform, not a validated intervention; (2)~\emph{formative, survey-grounded} design observations for the carpool module, whose generalizability awaits a separate driver-side study; and (3)~an auditable evidence pipeline whose output is a literature-synthesis tool, not an open-ended research agent. In particular, the $N{=}19$ driver-subset finding on rating-fairness sensitivity (\finding{5}) remains the paper's empirical anchor for the rating design, and the zero production ratings mean the soft launch can neither corroborate nor challenge it. The 184-user, 100\%-\edudot{}-verified registration cohort does lend modest support to the claim that \edudot{} scoping is tractable as a pure identity gate; it is silent on the harder question of whether that gate, plus the remaining primitives, translates into sustained carpool, marketplace, or activity participation.

\subsection{House of Quality: Mapping Findings to Features}\label{sec:hoq}

The five preceding deep-dive design decisions (\S\ref{sec:deep-dive}) and the soft-launch implementation snapshot (\S\ref{sec:deployment-feedback}) describe individual feature--evidence pairings. To make the relationships among them inspectable as a single artifact---and to give the continuous-optimization loop in \S\ref{sec:cont-opt} a structured input---we render the platform as a House of Quality (HoQ) matrix~\citep{HauserClausing1988, ChanWu2002}, mapping ten survey-derived customer requirements (WHATs) to twelve engineering characteristics (HOWs) drawn from \S\ref{sec:design-overview} and \S\ref{sec:deep-dive}. Figure~\ref{fig:hoq} shows the resulting matrix with relationship strength, roof correlations, implementation status, and a derived technical-importance row.

\begin{figure}[ht]
  \centering
  \includegraphics[width=\linewidth]{pic/v8_house_of_quality.pdf}
  \caption{House of Quality for \campusride{} v4.4. Rows (WHATs) are derived from formative survey findings F1--F6; columns (HOWs) are the design features specified against the deployed controllers, services, and database schema in \S\ref{sec:design}. Cell strength is $\bullet$\,$=$\,9 (strong), $\circledcirc$\,$=$\,3 (medium), $\circ$\,$=$\,1 (weak). The roof captures correlations between engineering characteristics: $\blacktriangle$\,$/$\,$\vartriangle$ for positive synergy and $\blacktriangledown$\,$/$\,$\triangledown$ for negative tension. The bottom row reports technical importance as $\sum_i (\text{WHAT}_i \times r_{ij})$ normalized to a percentage, expressing how much each engineering characteristic carries of the total customer-requirement weight.}
  \label{fig:hoq}
\end{figure}

\paragraph{Three readings of the matrix.} First, the technical-importance bar identifies four engineering characteristics that carry disproportionate weight: the WeChat cross-post bridge (EC9, $\sim$14\%), the \edudot{} email gate (EC1, $\sim$13\%), the auto-created ride-scoped group chat (EC8, $\sim$11\%), and the institution-domain whitelist (EC12, $\sim$10\%). Of these four, EC1 and EC8 are deployed and behaviorally exercised; EC9 is deployed and is in fact the largest production surface (82 \texttt{wxgroup\_notice\_record} rows, \S\ref{sec:deployment-feedback}); EC12 is the only \emph{pending} characteristic among the top four, which is the structural reason \S\ref{sec:multi-campus} treats multi-campus generalization as a near-term roadmap rather than a far-future direction. Second, the roof flags two negative correlations between rating-system primitives: bidirectional ratings (EC5) versus update-in-place revision (EC7) record a strong tension, and the 2-hour readiness delay (EC6) versus update-in-place a weaker one. Both reproduce the design caveats already disclosed in \S\ref{sec:dd-rating}: update-in-place is a one-line schema affordance whose interaction with rating fairness is structurally problematic and that the deployed system does not yet mitigate via dispute-window or trend-protection mechanisms. Third, the relationship matrix exposes \emph{cells of low coverage}: the customer requirement ``Post-trip resolution channel'' is supported only by EC7 (strong) and EC8 (medium), reflecting that current implementation expects update-in-place rating and ride-scoped chat to absorb both the fairness-revision and the lost-item / fare-correction use cases---a single-channel substitution which the limitation note in \S\ref{sec:dd-messaging} also flagged. Likewise, ``Transferable to other campuses'' is supported only by EC1 (strong) and EC12 (strong, pending), confirming that the platform's transferability surface is narrow and concentrated in the identity layer.

\paragraph{Scope of the HoQ.} We use HoQ as a \emph{readable summary} of the implemented design, not as a quantitative ranking exercise. The importance scores ($1$--$5$) are author-assigned mappings from the per-finding evidence pointers; the relationship strengths use the conventional $1/3/9$ encoding. The matrix is therefore a structuring tool that makes design-decision visibility tractable for a continuous review process; readers should not interpret a higher technical-importance percentage as empirical priority validated against deployment data. The pipeline-side counterpart of this matrix---the contradiction-map (\texttt{contradictions.json}, \S\ref{sec:pipeline-audit}), which surfaced the EC5/EC7 tension before the HoQ was rendered---is the load-bearing audit; the HoQ inherits its honesty calibration from that audit.

\paragraph{Companion MBSE artifacts.} Three standardized MBSE views complement the HoQ. Figure~\ref{fig:mbse-req-spec} formalizes the engineering characteristics EC1--EC12 as 12 ``the system shall'' requirements (R.1--R.12), each tagged with a subsystem chip, a verification method, and a row background reflecting deployment status (green = Deployed, yellow = Specified, red = Pending). Figure~\ref{fig:mbse-ahp} renders the priority weights derived from F1--F6 as a four-tier Analytical Hierarchy Process tree whose 10 composite leaves sum to 1.000. Figure~\ref{fig:mbse-trace} cross-tabulates the 10 most load-bearing requirements against the 8 active subsystems with \textbf{S}\,$=$\,satisfies and \textbf{V}\,$=$\,verifies cells plus a status / time-target right margin. Together these views make the requirement-to-subsystem and requirement-to-priority mappings inspectable as separate structured artifacts rather than as folded HoQ encodings.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_req_spec.pdf}
  \caption{Requirements specification R.1--R.12 anchored to HoQ EC1--EC12 (\S\ref{sec:hoq}). Status-tinted row backgrounds reflect the 2026-04-23 production snapshot: 10/12 Deployed (green), R.10 (cross-module points) Specified-not-deployed (yellow), R.12 (multi-institution domain whitelist) Pending (red). The Evidence column traces each requirement to a live row count or controller artifact.}
  \label{fig:mbse-req-spec}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_ahp_objectives.pdf}
  \caption{Analytical Hierarchy Process for the v4.4 design objectives. Three top-level criteria (User Experience \& Trust 0.50, Operational Efficiency \& Reach 0.33, Cost-Sharing \& Sustainability 0.17) decompose into 10 sub-criteria; the bottom row shows the composite priority weights (top $\times$ sub) that sum to 1.000. The stacked bar at the bottom ranks the 10 composite priorities for direct comparison.}
  \label{fig:mbse-ahp}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_traceability_matrix.pdf}
  \caption{Requirements $\times$ Subsystem traceability matrix. Rows: 10 load-bearing requirements R.1--R.10. Columns: 8 active subsystems (Auth, Ride-Match, Cost-Split, SOS-Safety, Schedule, Comm/Chat, Suggest-Alt, Monitor/Reward). Filled blue \textbf{S} = subsystem satisfies the requirement; hollow orange \textbf{V} = subsystem verifies it. Right-margin Status badges (Active/Specified/Pending) and Time Target columns inherit from the deployment snapshot.}
  \label{fig:mbse-trace}
\end{figure*}

\subsection{MBSE Risk Analysis and Verification Trace}\label{sec:risk-vv}

The HoQ flags engineering-characteristic priorities; a complementary risk view is needed to track \emph{where the design can fail} and \emph{how each requirement is verified}. We adopt two standardized Model-Based Systems Engineering views---a Failure Mode Effects Analysis~\citep{Stamatis2003} and a verification matrix~\citep{INCOSE2015}---rendered over the same 2026-04-23 snapshot. These complement the standardized BDD/IBD/FFBD/sequence/activity views in \S\ref{sec:design-overview}--\S\ref{sec:carpool-overview} (notation per UML 2.5.1~\citep{OMG_UML_2017} and SysML~\citep{Friedenthal2014}) and the AHP priority decomposition in Figure~\ref{fig:mbse-ahp}~\citep{Saaty1980}; together they situate the v4.4 design inside the standard MBSE documentation surface without claiming any MBSE methodology contribution---the MBSE views are a structuring lens, not a thesis.

\paragraph{Failure Mode Effects Analysis.} Figure~\ref{fig:mbse-fmea} enumerates 12 v4.4 failure modes anchored to live subsystems, each with a Severity, Occurrence, and Detection score (1--5) and a Risk Priority Number RPN\,$=$\,S$\times$O$\times$D heat-tinted in the rightmost numeric column. The four highest-RPN rows are: SOS Safety button not yet wired to emergency contacts (RPN\,60), Cost-Splitting / payment integration not deployed (RPN\,48), the F5-validated rating-fairness retaliation risk under update-in-place revision (RPN\,24, \S\ref{sec:dd-rating}), and Group Discovery funnel stalled at 1-member-per-group (RPN\,24, \S\ref{sec:groups}). The five-mitigated-low-risk rows reflect mechanisms already in place---the silent swallow of duplicate-key 23505 on the ride-scoped group ensure (\S\ref{sec:dd-messaging}) is the canonical example. The FMEA is descriptive, not predictive: the Occurrence scores are author estimates from code-path inspection, not measured incident frequencies.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_fmea_table.pdf}
  \caption{Failure Mode Effects Analysis: 12 v4.4 subsystem failure modes with Severity / Occurrence / Detection (1--5 each) and Risk Priority Number RPN\,$=$\,S$\times$O$\times$D heat-tinted. The four highest-risk rows (SOS RPN\,60; Payment integration 48; F5-validated rating retaliation 24; Group discovery funnel 24) define the near-term release backlog complementary to \S\ref{sec:cont-opt}.}
  \label{fig:mbse-fmea}
\end{figure*}

\paragraph{Verification matrix.} Figure~\ref{fig:mbse-verif} cross-tabulates 12 test procedures (TP.1--TP.12) against the 10 originating requirements (OR.1--OR.25 corresponding to EC1--EC10 from the HoQ, preserving the OR-id pattern of the standardized template). The diagonal `\texttt{x}' pattern represents one-test-per-requirement coverage; TP.11 (manual snapshot inspection 2026-04-23) covers six EC requirements simultaneously and is the lowest-cost verification surface in current operation; TP.12 (E2E happy-path browser test) is the only Pending row and is the structural prerequisite for moving from formative deployment to operational evaluation.

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_verification_matrix.pdf}
  \caption{Verification matrix: 12 test procedures TP.1--TP.12 (rows) $\times$ 10 originating requirements OR.1--OR.25 (columns) with the diagonal `\texttt{x}' verification pattern. TP.11 (manual snapshot inspection 2026-04-23, Inspection method) covers 6 EC requirements; TP.12 (E2E happy-path browser test, Demo method) is Pending. Verification methods are colour-chipped (Test/Inspection/Demo/Analysis); Status column is green Deployed / red Pending.}
  \label{fig:mbse-verif}
\end{figure*}

\subsection{Continuous Optimization Loop}\label{sec:cont-opt}

The deployment snapshot reported in \S\ref{sec:deployment-feedback} is one tick of an intended sustained loop, not a one-shot evaluation. We treat the soft launch as the start of a continuous-optimization process whose three coupled feedback channels are already instrumented in the deployed schema and whose review cadence is anchored on the HoQ artifact in \S\ref{sec:hoq}.

\paragraph{Telemetry channels (already deployed).} \emph{Registration cadence.} Monthly \texttt{users} insertions for the pilot window were 3 (Jan), 70 (Feb), and 111 (March), measured against a constant outreach effort (the WeChat-group push channel described below). The cadence yields a directional signal of acquisition response and is the simplest growth observable. \emph{Notification fan-out.} The \texttt{notifications} table accumulated 54 rows across ten event types whose distribution (Table~\ref{tab:notifs}) is consistent with a designed 5+2 bundle per booking; this is residual evidence of historical ride transactions even when the corresponding \texttt{rides} / \texttt{ride\_bookings} rows have been cleaned, which makes notifications a more durable health metric than the transactional tables themselves. \emph{Grassroots bridge counter.} \texttt{wxgroup\_notice\_record} accumulated 82 rows (62 marketplace, 16 ride, 4 activity) and is the single largest production surface; its module split is itself a usage-mix metric that does not require user retention to register. \emph{User feedback channel.} The \texttt{system\_messages} table with \texttt{sender\_type='user'} and \texttt{message\_type='feedback'} (10 rows in the snapshot, all dated 2026-01-10 to 2026-02-11) is a low-volume but qualitatively rich signal that we triage manually in each review cycle.

\paragraph{Review cadence.} We adopt a monthly snapshot review whose work product is a small set of release-eligible items and a refreshed copy of Figure~\ref{fig:hoq}. Each review reads the four telemetry channels, scans the \texttt{system\_messages} feedback inbox, re-runs the contradiction-map step of the \researchagent{} pipeline (\S\ref{sec:pipeline-arch}) on any new literature added in the period, and compares the result against the HoQ. The HoQ is the structural surface on which optimization decisions are recorded: each release-eligible item is keyed to one or more cells (CR$_i$ $\times$ EC$_j$) whose status moves toward \emph{deployed} or whose relationship strength changes as the implementation tightens. This pattern echoes in-the-wild and continuous-engagement practice in HCI field studies~\citep{Brown2011wild, Rogers2017wild}, with the qualification that our metrics are operational signals rather than experimental measurements.

\paragraph{Three near-term release tracks, surfaced by the matrix.} (1)~The points subsystem (EC10, status \emph{specified} in Figure~\ref{fig:hoq}, with $\sim$5\% technical importance) is implementation-ready in the controller layer (\S\ref{sec:dd-gamification}) but not yet deployed; provisioning \texttt{point\_rules} and creating \texttt{point\_transactions} would lift its status without additional UX work, even though the relatively low importance share argues that this is not the highest-priority release track. (2)~The EC5 $\times$ EC7 negative roof correlation (Figure~\ref{fig:hoq}, top), already disclosed in \S\ref{sec:dd-rating} as the dispute-window / trend-protection / mandatory-justification gap, is a candidate for a release in which update-in-place is constrained by either a time-bounded dispute interval or a stricter ratee-consent path. (3)~The institution-domain whitelist (EC12, status \emph{pending}, $\sim$10\% technical importance) is the structural prerequisite for the multi-campus expansion in \S\ref{sec:multi-campus} and is in this sense the highest-leverage of the three release tracks, since it unblocks customer requirement CR10 (``Transferable to other campuses'') whose current relationship row is sparse.

\paragraph{Loop, not score.} We frame this as a loop rather than a score because no single number aggregates well across the four telemetry channels, the HoQ matrix, and the qualitative feedback inbox. The artifact-level honesty discipline (Phase~5 evaluation, \S\ref{sec:pipeline-arch}) is preserved at the loop level: each review cycle is required to re-state the implementation-versus-claim alignment that \S\ref{sec:pipeline-audit} (third negative-audit instance) instituted for the design-decision text, so that subsequent revisions of \S\ref{sec:dd-rating} or \S\ref{sec:dd-gamification} cannot quietly fall out of sync with the deployed schema.

\section{Research-Agent Pipeline as Methodology Contribution}\label{sec:pipeline}

\subsection{Architecture and Eight-Phase Flow}\label{sec:pipeline-arch}

The pipeline uses a provider layer (OpenAlex, Semantic Scholar, arXiv, Lens, Crossref), a reasoning layer (Claude and GPT models tiered by task complexity), an identity layer (DOI-based canonical IDs), a state machine (phase-based resumability), and a contract layer enforcing structural invariants across phases. The eight phases are: (1)~Corpus Assembly, (2)~Classification into a ten-category taxonomy (A--J), (2.5)~Deep Extraction of claims, methods, and findings, (3)~Relationship Graph with evidence-sufficiency diagnostics, (3.5)~Narrative Chain generation per beat, (3.7)~Contradiction Map, (4)~Evidence Inventory, and (5)~Five-Reviewer Evaluation (narrative, coverage, gap, contradiction, and honesty reviewers, each scoring independently).

\subsection{Audit Trail: How the Pipeline Shaped This Paper}\label{sec:pipeline-audit}

\paragraph{Positive audit instances.} The anchor papers for \S\ref{sec:related} were selected from the pipeline's \texttt{narrative\_chains.json}. The five adversarial-scoping paragraphs in \S\ref{sec:discussion-limits} directly map to the five focus areas in the pipeline's \texttt{contradictions.json}. The finding cross-references in \S\ref{sec:deep-dive} (\finding{3}$\times$3, \finding{4}$\times$1, \finding{5}$\times$1, \finding{6}$\times$1) were verified against the \texttt{evidence\_inventory.json} coverage check. Phase~5 reviewer feedback drove iterative revision: for instance, an early draft's use of ``effective'' in \S\ref{sec:dd-rating} was flagged by the honesty reviewer and replaced with ``designed to address''; a subsequent pass rewrote the subsection against the actual implementation (see the third negative-audit instance below), improving the honesty score from 0.72 to 0.88.

\paragraph{Negative audit instances.} The pipeline also produced misleading signals that required human correction. First, Phase~2 automated classification labeled three proxy-level papers as native Category~E (\edudot{}-scoped identity verification); manual audit (documented in \texttt{config/e\_category\_audit.md}) downgraded them and replaced them with six Crossref-validated native E papers~\citep{Ellison2007, Ellison2014, Schlesinger2017, Black2016, Heston2016, Wu2017}. Second, the initial evidence inventory for \finding{5} reported driver tolerance on the full mixed sample ($N{=}30$); subset analysis revealing that the rating-fairness asymmetry is concentrated in the Driver/Both subset ($N{=}19$) was performed manually, exposing a scope boundary of the pipeline: it does not automatically perform subset sensitivity analysis on primary survey data. Third, an earlier draft of \S\ref{sec:dd-rating} described a ``pre-publication dispute window (e.g., 24~hours)'' and a ``cross-trip trend protection'' clause. A direct read of the implemented \texttt{rating.controller.js} and the \texttt{ratings} / \texttt{users} schemas showed that neither is present: the live system enforces only a 2-hour post-departure rating-readiness delay and an unweighted-mean aggregation, with update-in-place as the only revision path. The subsection was rewritten to match the deployed mechanism and to flag the dispute-window / trend-protection ideas as open design proposals---an alignment that the pipeline, which works abstract-first over prior literature rather than over the codebase, does not enforce. Fourth, a first draft of \S\ref{sec:deployment-feedback} reported numbers from the repo's \texttt{.env.production} Supabase project (\texttt{jfgenxnqpuutgdnnngsl}), which turned out to be a superseded staging / demo database seeded with showcase content (one demo driver, 8 fabricated rides, a \texttt{point\_transactions} table populated by registration bonuses). The Railway deployment actually binds to a different Supabase project (\texttt{bwimyvkwkenrtumsfjzt}), whose credentials live only in the Railway environment. After being handed the production keys we re-queried, which swapped 72 users / 8 rides / 65 point transactions for 184 users / 0 currently-live rides / a points subsystem that is not deployed at all. The paper now reports the Railway-backed numbers, and this mismatch is recorded here as a caution: ``production'' markers in a repo's environment file are not load-bearing without a deployment-side cross-check. Fifth, the v4.4 corpus expansion (HoQ, multi-campus, and continuous-deployment topics) used a topical vocabulary filter to compress an unfiltered $\sim$10{,}000-paper retrieval pool to a 500-paper working set; classification then assigned 17 of 93 candidates to Category~X (no fit), including off-topic results such as nursing workforce reports, autonomous-vehicle surveys, blind-stick assistive devices, and big-educational-data architecture papers that nonetheless contained surface-level vocabulary matches (e.g., ``mobility,'' ``platform''). Manual review confirmed Category~X was assigned correctly in all 17 cases; the false positives entered through topical-vocabulary lexical overlap rather than misclassification. We marked them \texttt{pruned=true} (an append-only flag rather than deletion) so downstream phases skip them, and we record this here because it surfaces a concrete pipeline limit: a vocabulary-based topical filter, even one tuned to the project's ten-category taxonomy, will admit lexical-overlap noise and requires an explicit downstream gate (in our case, the Phase~2 classifier's Category~X label) to exclude it from analysis.

\paragraph{Reproducibility.} The pipeline's full configuration, \texttt{state.json}, phase-level artifacts, and audit logs (including Prompt~A/B/E audit records) are open-sourced at the project repository.

\subsection{Scope and Honest Limitations of the Pipeline}\label{sec:pipeline-limits}

The pipeline is not an open-ended research agent, an automated thesis generator, or a gap-discovery tool (its \texttt{gaps\_ranked.json} output is a diagnostic signal, not a conclusion). It operates abstract-first and does not perform full-text truth extraction. It does not perform subset robustness checks on primary survey data, requiring human intervention for analyses such as the Driver/Both vs.\ Rider-only split reported in \S\ref{sec:findings-driver}. It also does not cross-check design claims in the manuscript against the implemented codebase or deployed schema---the mechanism correction in \S\ref{sec:dd-rating} was performed manually by inspecting \texttt{rating.controller.js}, the \texttt{ratings} table DDL, and the live \texttt{point\_rules} catalog, and is recorded as the third negative-audit instance above. We recommend that future users treat it as a structuring and auditing complement to human judgment, not as a replacement, and that design-case papers pair it with an explicit implementation-versus-manuscript reconciliation pass.

\section{Discussion}\label{sec:discussion}

\subsection{General Reflections}\label{sec:discussion-general}

\paragraph{From grassroots to formal.} \edudot{} verification occupies a middle ground between commercial rideshare platforms (where identity is verified but community is absent) and informal WeChat groups (where community exists but identity is unverified). \campusride{} positions institutional identity as a third trust architecture---one that is scoped by shared affiliation rather than by market participation or social proximity.

\paragraph{Cross-module transferability.} The four design primitives are not carpool-specific. The identity layer is shared across all six modules; the messaging embedding creates cross-module coordination channels; and the points meta-layer links incentives across modules. This suggests a methodological claim: design primitives distilled from one module's deep-dive can propagate to other modules within the same identity-scoped platform, though we acknowledge that only the carpool module received deep-dive treatment and the others remain at overview level.

\paragraph{Pipeline-assisted design research.} The \researchagent{} pipeline made the literature synthesis auditable and pushed adversarial scoping deeper than it would have been otherwise: the contradiction reviewer identified five focus areas that directly structured \S\ref{sec:discussion-limits}. At the same time, the pipeline's limitations---niche-category misclassification, absence of primary-data sensitivity analysis, and no implementation-versus-manuscript reconciliation---required manual correction, reinforcing that the pipeline is a complement to, not a substitute for, human judgment.

\paragraph{What the soft launch taught us.} The $\sim$4-month soft launch on \texttt{www.campusgo.college} (\S\ref{sec:deployment-feedback}) reshaped the manuscript in three ways that a design-without-deployment version could not have. First, inspecting the live \texttt{ratings}, \texttt{rides}, and \texttt{point\_rules} tables against \S\ref{sec:deep-dive} surfaced the rating-mechanism overclaim corrected in \S\ref{sec:dd-rating}: the implemented system enforces a 2-hour post-departure readiness delay, role-paired submission, and update-in-place revision, with neither a formal dispute window nor trend protection. Second, querying the Railway-backed production project exposed a deployment-versus-repo gap: the points subsystem (\S\ref{sec:dd-gamification}), fully specified in backend code, has zero \texttt{point\_rules} rows and no \texttt{point\_transactions} table in production, and all 184 user rows have \texttt{users.points = 0}. The gamification primitive is therefore a code-level affordance, not yet a behavioral lever; we surface this rather than paper over it. Third, the asymmetry between identity registration (184 verified \texttt{@cornell.edu} accounts) and module engagement (zero currently-live rides, activities, or ratings; 15 removed marketplace items; 5 single-member community groups) sharpens the cross-module framing: even a fully functional \edudot{} gate does not spontaneously produce content on the other side. The WeChat notice bridge (82 pushes: 62 marketplace, 16 rideshare, 4 activity) is where the platform reaches back into the grassroots channels that the formative survey named, and is the surface where historical ride bookings left their most legible traces. These are formative observations, not deployment validations; none changes the paper's contribution claims.

\subsection{Toward Multi-Campus Generalization}\label{sec:multi-campus}

The HoQ in \S\ref{sec:hoq} flags ``Transferable to other campuses'' as a customer requirement that the current implementation supports only narrowly: through the \edudot{} email gate (EC1, deployed as Cornell-only) and the institution-domain whitelist (EC12, pending). Whether \campusride{} extends to a different campus is therefore an open design question, not a settled engineering problem. We separate the answerable substructure into three components: what is genuinely Cornell-specific in the present design, what is plausibly structural and re-usable, and what an honest onboarding playbook for a second campus would require.

\paragraph{What is Cornell-specific.} (a) \emph{The Ithaca transit-gap profile.} Findings F1--F1b (\S\ref{sec:findings-passenger}) describe a small-city, small-student-population, sparse-rideshare context. They are unlikely to transfer unchanged to commuter-heavy campuses (where private-vehicle ownership dominates) or to transit-dense urban campuses (where the gap is shaped by metropolitan transit pricing rather than rideshare availability). (b) \emph{The grassroots channel.} Our survey's grassroots observation (17 of 21 Mandarin-native respondents who answered the carpool-finding question used WeChat / WhatsApp groups) is shaped by Cornell's specific international-student composition; at a campus with a different cohort mix the grassroots bridge in \S\ref{sec:rw-grassroots} might be Discord servers, Telegram channels, or Reddit campus-subreddits, with different moderation and discovery dynamics~\citep{Liu2023, Bonini2023}. (c) \emph{The Cornell-specific email domain.} The \edudot{} gate is presently coded as \texttt{@cornell.edu}; multi-campus operation requires the institution-domain whitelist (EC12) and a per-cohort routing primitive that the present database schema does not yet model. (d) \emph{F5's specific carpool culture.} The driver-side rating-fairness asymmetry (\finding{5}) was observed in a Cornell carpool-leaning international-student subset ($N{=}19$); whether occasional drivers at other campuses exhibit the same pattern is an empirical question that requires a per-campus survey, not a deployment hypothesis.

\paragraph{What is plausibly structural.} The four design primitives distilled in \S\ref{sec:rw-primitives}---institutional identity verification, in-trip safety infrastructure, rating-fairness considerations, and gamification rewards as secondary motivation---are derived from a literature that is broader than any single campus. The HoQ structure itself (\S\ref{sec:hoq}) is a re-usable artifact whose customer requirements would be re-populated from a per-campus survey but whose engineering characteristics, relationship encoding, and roof-correlation discipline transfer directly. The \researchagent{} pipeline (\S\ref{sec:pipeline}) is a methodology, not an Ithaca-bound tool: its eight-phase flow, ten-category taxonomy, and five-reviewer evaluation are domain-agnostic and we have used the same pipeline on prior thesis drafts in unrelated subject matter. The cross-module embedding pattern in \S\ref{sec:dd-messaging} (auto-created scope-bound group chat that materializes alongside transactional rows) is a generic CSCW pattern and is not Cornell-specific.

\paragraph{Onboarding playbook for a second campus.} An honest pilot at a peer institution requires four pre-deployment steps, not a code clone. (1)~A formative survey, six to twelve weeks, large enough to populate the HoQ rows under that campus's transit, demographic, and grassroots-channel conditions; we do not recommend reusing Cornell's WHATs without local re-elicitation. (2)~An institution-domain whitelist deployment (EC12) plus a per-cohort routing primitive in the database schema; the schema currently treats \texttt{users.university} as a free-form string, which is structurally inadequate for multi-cohort operation. (3)~A grassroots-channel localization step: the WeChat outreach path (\S\ref{sec:dd-messaging}, \texttt{wxgroup\_notice\_record}) must be re-targeted to whatever channels carry that campus's day-to-day coordination, and the cross-post format must be re-localized. (4)~A monthly continuous-optimization loop (\S\ref{sec:cont-opt}) anchored on a per-campus HoQ refresh, run for at least one academic semester before scale claims. None of these four steps is technically novel; the point is that they constitute the minimum honest scoping for a second deployment.

\paragraph{Risks of premature transfer.} Three risks are worth flagging. \emph{Generalization without local survey.} Replicating the design without re-doing the formative work would re-introduce precisely the honesty issue that the pipeline's contradiction reviewer was built to surface (\S\ref{sec:pipeline-audit}). \emph{Replication of F5 is not assumed.} The driver-side rating-fairness asymmetry rests on a small subset and we explicitly do not predict it will replicate; if it does not, that is a finding, not a failure. \emph{Federation is not in scope.} Multi-campus operation as separate single-campus instances is a near-term roadmap; cross-campus rides, cross-campus identity recognition, and inter-institutional governance are out-of-scope for the present design and would require additional schema, policy, and HoQ work~\citep{Mufumbiro2026}.

\subsection{Adversarial Scoping and Limitations}\label{sec:discussion-limits}

\paragraph{Formalization risk.} Formalizing grassroots coordination practices into a platform may reproduce the opacity, autonomy loss, and asymmetrical oversight associated with algorithmic management~\citep{Keegan2025, Kinowska2022, Weber2023}. Our rating-fairness design (\S\ref{sec:dd-rating}) is a \emph{response} to this risk, not a \emph{solution}; whether it prevents the emergence of platform-mediated harm remains untested.

\paragraph{Three-layer sample skew.} Our findings are scope-limited by three layers of sample skew: (a)~\emph{Language skew}: 72 of 91 respondents reporting native language (79\%) were Mandarin-native; only 15 (16\%) were English-native. Any claim about English-speaking students---including that they do not use WeChat groups---carries substantial uncertainty. (b)~\emph{Driver-subset skew}: The \finding{5} rating-fairness asymmetry rests on the Driver/Both subset ($N{=}19$), which is methodologically preferred over the full-sample mix but still small and requires a dedicated driver-side survey to confirm. The Rider-only control ($N{=}11$--12) is reported for transparency, not because its weaker pattern invalidates the finding. (c)~\emph{Completion skew}: Only 44 of 111 eligible respondents (40\%) completed the full survey; finishers may differ systematically from non-finishers in carpool salience or engagement.

\paragraph{No deployment evaluation.} This paper stops at the design-case stage. The four carpool design decisions have not been compared in a deployed setting, and any claim about their relative effectiveness remains design-motivated rather than usage-validated~\citep{Tushev2022, Fradkin2021}.

\paragraph{Scope boundary of \edudot{}.} \edudot{} verification confirms institutional affiliation; it does not verify driving competence, safe conduct, legal accountability, or governance quality~\citep{Mufumbiro2026}. Identity verification addresses identity problems but not behavior problems, and it does not substitute for platform governance.

\paragraph{Gamification risk.} Cross-module points may invite gaming rather than trustworthy participation: points can become targets in themselves, creating incentives for fake trips, strategic compliance, or pressure-inducing behavior~\citep{Cheon2025, Zhang2025algo}. Work-games and algorithmic-control studies make such gaming plausible~\citep{Wu2026algo}, but we do not claim measured abuse in \campusride{} itself.

\section{Conclusion}\label{sec:conclusion}

Small-town campuses present a multi-faceted coordination gap that extends beyond transportation; international students' grassroots practices give this gap a concrete shape. \campusride{} formalizes these practices into a six-module identity-verified platform, sharing four design primitives across carpool, marketplace, activities, groups, messaging, and points modules. The five design decisions in the carpool deep-dive are specified against the deployed controllers, services, and schemas that back them, and are situated against a $\sim$3.5-month soft launch on \texttt{www.campusgo.college} (184 verified Cornell users; zero currently-live rides, ratings, or points transactions) whose 2026-04-23 snapshot we report as formative implementation signal rather than as evaluation. The Driver/Both-subset rating-fairness observation (\finding{5}) remains the paper's most counterintuitive contribution: occasional campus drivers are least tolerant of rating-system unfairness, not of passenger behavioral misbehavior. The \researchagent{} pipeline, contributed as an open-source methodology tool, provides an auditable evidence chain for design-research literature synthesis, including systematic contradiction surfacing for honest scoping, and its limits---including the absence of an implementation-versus-manuscript reconciliation---are reported alongside its use.

\bibliographystyle{plainnat}
\bibliography{bib}

\end{document}