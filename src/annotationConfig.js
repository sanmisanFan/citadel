export const anomalousColorScheme = {
  citation: {
    baseColor: "rgba(197,27,138,1)",
    boxColor: "rgba(197,27,138,0.3)",
    category: {
      lowRelevancy: {
        baseColor: "rgba(247,104,161,1)",
        boxColor: "rgba(247,104,161,0.3)"
      },
      retractedPaper: {
        baseColor: "rgba(251,180,185,1)",
        boxColor: "rgba(251,180,185,0.3)"
      },
      selfCitation: {
        baseColor: "rgba(255,127,14,1)",
        boxColor: "rgba(255,127,14,0.3)"
      },
      citationRing: {
        baseColor: "rgba(214,39,40,1)",
        boxColor: "rgba(214,39,40,0.3)"
      },
      unreferenced: {
        baseColor: "rgba(140,140,140,1)",
        boxColor: "rgba(140,140,140,0.3)"
      }
    }
  },
  statistic: {
    baseColor: "rgba(217,95,14,1)",
    boxColor: "rgba(217,95,14,0.3)",
    category: {
      testFailure: {
        baseColor: "rgba(254,196,79,1)",
        boxColor: "rgba(254,196,79,0.3)"
      },
      valueInconsistency: {
        baseColor: "rgba(255,247,188,1)",
        boxColor: "rgba(255,247,188,0.3)"
      }
    }
  },
  other: {
    baseColor: "rgba(37,52,148,1)",
    boxColor: "rgba(37,52,148,0.3)",
    category: {
      valueInconsistency: {
        baseColor: "rgba(44,127,184,1)",
        boxColor: "rgba(44,127,184,0.3)"
      },
      noRef: {
        baseColor: "rgba(65,182,196,1)",
        boxColor: "rgba(65,182,196,0.3)"
      }
    }
  }
};