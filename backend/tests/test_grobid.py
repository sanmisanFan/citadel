from CITation.data.grobid import parse_citation_mentions, parse_tei_references


def test_parse_citation_mentions_prefers_visible_label_over_target_id():
    tei_xml = """
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
      <text>
        <body>
          <p coords="3,10,10,500,20">
            Existing automated tools only partially address these problems.
            StatReviewer <ref type="bibr" target="#b6" coords="3,100,10,20,10">[32]</ref>
            and statcheck <ref type="bibr" target="#b7" coords="3,150,10,20,10">[22]</ref>
            target statistical reporting errors.
          </p>
        </body>
      </text>
    </TEI>
    """

    mentions = parse_citation_mentions(tei_xml)

    assert 32 in mentions
    assert 22 in mentions
    assert 7 not in mentions
    assert 8 not in mentions
    assert mentions[22][0]["page"] == 3
    assert "statcheck" in mentions[22][0]["text"]


def test_parse_citation_mentions_handles_multi_ref_group_with_punctuation():
    """``[22,30,32]`` is emitted by GROBID as three sibling ``<ref>`` tags
    whose visible labels are ``"[22,"``, ``"30,"``, and ``"32]"``. The
    fullmatch-only label parser used to return ``None`` for the first two
    (trailing comma) and fall back to the target attribute, which can be
    off-by-one. The leading-digit regex now binds each marker to the
    visible number even when surrounded by list punctuation.
    """
    tei_xml = """
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
      <text>
        <body>
          <p coords="2,10,10,500,20">
            Overlap detectors and statistical auditors
            <ref type="bibr" target="#b20" coords="2,100,10,15,10">[22,</ref>
            <ref type="bibr" target="#b28" coords="2,120,10,15,10">30,</ref>
            <ref type="bibr" target="#b30" coords="2,140,10,15,10">32]</ref>
            catch surface errors.
          </p>
        </body>
      </text>
    </TEI>
    """

    mentions = parse_citation_mentions(tei_xml)

    assert 22 in mentions
    assert 30 in mentions
    assert 32 in mentions
    # Off-by-one target ids (#b20/#b28) should NOT have been used.
    assert 21 not in mentions
    assert 29 not in mentions
    for ref_num, expected_label in [(22, "[22,"), (30, "30,"), (32, "32]")]:
        occ = mentions[ref_num][0]["occurrences"][0]
        assert occ["ref_label"] == expected_label
        assert occ["page"] == 2


def test_parse_tei_references_uses_numeric_label_for_ref_id():
    tei_xml = """
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
      <listBibl>
        <biblStruct>
          <label>[22]</label>
          <analytic>
            <title level="a">statcheck</title>
            <author>
              <persName>
                <forename>Michèle</forename>
                <surname>Nuijten</surname>
              </persName>
            </author>
          </analytic>
          <monogr>
            <title level="j">None</title>
          </monogr>
          <imprint>
            <date when="2014" />
          </imprint>
        </biblStruct>
      </listBibl>
    </TEI>
    """

    parsed_refs, _ = parse_tei_references(tei_xml)

    assert len(parsed_refs) == 1
    assert parsed_refs[0]["ref_id"] == 22
    assert parsed_refs[0]["title"] == "statcheck"
