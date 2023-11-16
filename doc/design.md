Design notes
============

> Utility design sketches

Items
-----

__Test:__

- `name`
- `tags`
- `input`
- `golden_stdout`
- `golden_stderr`
- `golden_file_output`

__TestOutput:__

- `actual_stdout`
- `actual_stderr`
- `actual_file_output`

__Result__ = (`Test`, `TestOutput`)

__Pipeline:__ () ⟶ unit = TestDiscovery ➔ Runner ➔ List[Exporter]

```
Framework.run(pipelines: List[Pipeline])
```

__Test Discovery:__ ((testtags: List[tag]) ⟶ bool) ⟶ List[Test]
__Runner:__ (List[Test]) ⟶ List[Result]
__Exporter:__ List[Result] ⟶ unit

Modules
-------

1. Comparison API
2. Test Discovery
3. Runner
4. UpdateExporter
5. DiffExporter

`BeforeAll`, `AfterAll`, `BeforeEach`, `AfterEach`
