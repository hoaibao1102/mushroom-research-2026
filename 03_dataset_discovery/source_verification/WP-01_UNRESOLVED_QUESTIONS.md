# WP-01: Unresolved Scientific & Technical Questions

**Tracking Log:** Open issues identified during WP-01 evidence verification.  
**Policy:** Unresolved questions must be addressed prior to dataset selection (Gate G1) or baseline reproduction (Gate G2).  

---

## Priority 1 — Critical Selection Blockers (Must resolve before dataset selection)

1. **C02 Annotation JSON Payload on Kaggle:**  
   - *Question:* Where are `MushR_coco_annotations_train.json` and `MushR_coco_annotations_test.json` located? Are they packaged inside an archive on Kaggle, hosted in a separate release, or omitted from the public Kaggle files API listing?
   - *Impact:* If COCO instance annotations are missing from the public download, C02 cannot be trained for instance segmentation.
2. **C01 Bag-Level Metadata and Data Leakage:**  
   - *Question:* Does Mendeley dataset `jrbx34k77g/2` contain image EXIF data, bag IDs, or timestamps that allow grouping multiple photos of the same physical bag?
   - *Impact:* If 761 images represent repeated shots of only 20–30 bags, random train/test splitting will produce invalid, highly inflated accuracy.
3. **C02 Class Schema Mismatch (3 vs 4 Classes):**  
   - *Question:* Why does author code `train_net.py` define 4 classes (`Pinning`, `Not-Ready`, `Ready`, `Overdue`), whereas the published paper evaluates only 3 classes (`Not-Ready`, `Ready`, `Overdue`)? How was the `Pinning` class handled during evaluation?

---

## Priority 2 — Methodological & Reproducibility Questions (Must resolve before baseline training)

4. **C01 Biological Ground Truth & Pathogen Identity:**  
   - *Question:* Was any laboratory culture or PCR test performed to confirm whether "green mold" was *Trichoderma* and "black mold" was *Aspergillus* / *Rhizopus*, or was labeling entirely subjective?
   - *Impact:* Determines whether the model learns real fungal pathology or simply surface color variations.
5. **C02 Detectron2 Runtime Environment Pinning:**  
   - *Question:* Can the author's Detectron2 repository be executed in a modern environment (PyTorch 2.x, CUDA 12.x) without building legacy CUDA extensions, or is a containerized legacy environment (PyTorch 1.10 / CUDA 11.3) required?
6. **C02 Test Split Independence:**  
   - *Question:* Did the authors partition train and test sets by grow tent / flush cycle / time period, or by random image selection across the 10-month hourly camera feeds?

---

## Priority 3 — Real-World Farm Deployment Questions

7. **Lens Fogging & Spore Fouling in Oyster Mushroom Farms:**  
   - *Question:* Oyster mushroom fruiting requires 85–95% relative humidity and releases billions of spores daily. How can an optical camera setup be maintained in a real farm without daily manual lens cleaning?
8. **Alternative Non-ML Solutions for Contamination:**  
   - *Question:* Could CO2 and VOC gas sensors detect anaerobic bacterial or fungal substrate rot faster and more reliably than external surface vision?
