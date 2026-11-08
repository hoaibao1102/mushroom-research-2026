# Domain and application questions — Day 6

These are implementation questions to resolve through data inspection and, later, field testing.

## Capture and cultivation layout

- What is the exact grow-unit hierarchy in deployment: farm/room → batch → column/rack → shelf/tray/bag → camera view?
- Does a camera remain fixed for the full cultivation cycle, or can it be moved/repositioned?
- Is there one camera per column, one camera viewing several columns, or multiple views per grow unit?
- Are captures strictly daily, or can the capture interval vary? How will local timestamps and daylight-saving/timezone details be stored?
- Can harvest, bag replacement, contamination cleaning or other interventions be logged as events?

## Recognition and tracking

- Which mushroom species are expected at the deployment site? Which species need to be recognized at launch versus later?
- Is the primary unit a whole visible cluster/flush or each individual fruitbody? The initial system uses cluster-level tracking where the camera scene supports it.
- How much camera motion, occlusion, growth overlap and partial harvesting occurs in the target scene?
- Can each image be mapped reliably to a camera and fixed grow-unit ID?
- Does general `mushroom` detection suffice initially, with species and maturity optional, or is species identification required from the first release?

## Measurement and maturity

- Is relative pixel-area/box growth sufficient for the first release?
- Can a known-size marker be placed in the camera view, or can camera intrinsics and distance be calibrated?
- Which maturity stages are meaningful for each cultivated species, and who will adjudicate labels?
- Should maturity use source-specific labels (e.g. not-ready/ready/overdue) or a normalized site-defined scale?

## Data and model updates

- Which public datasets are useful after visual inspection of their actual collection geometry and annotation format?
- Which target-scene samples are needed to close the gap between published datasets and vertical-column/horizontal-camera scenes?
- How many reviewed examples per species, view, stage and growth condition are needed before each model release?
- What fixed regression set will protect against forgetting when the model is updated?
- Which uncertainty or disagreement signals should select daily samples for human review?

## Runtime

- Can the selected exported model run on the RX 5500 XT through DirectML, or will CPU be the reliable first runtime?
- What resolution and throughput are acceptable for one daily capture per configured view?
- Does the target OS support the chosen ONNX Runtime DirectML installation, and do all exported model operators execute correctly?

**Current evidence level:** requirements are based on the user's project brief. No real target-farm sequence has yet been provided or field-validated.
