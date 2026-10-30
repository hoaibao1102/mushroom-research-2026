"""Lossless compact QC relation from same inventory, replacing oversized derived JSON only."""
from pathlib import Path
import json,collections,math
Q=Path('D:/Capstone/mushroom-research-2026/04_dataset_candidates/C03_agaricus_disease/qc'); rows=json.loads((Q/'inventory.json').read_text()); buckets=collections.defaultdict(list); exact=collections.defaultdict(list)
for r in rows: buckets[r['dhash64']].append(r['path']); exact[r['sha256']].append(r['path'])
items=sorted(buckets.items()); edges=[]; count=0
for i,(a,pa) in enumerate(items):
 if len(pa)>1: edges.append([a,a,0,len(pa)*(len(pa)-1)//2]); count+=edges[-1][3]
 for b,pb in items[i+1:]:
  dist=(int(a,16)^int(b,16)).bit_count()
  if dist<=4: edges.append([a,b,dist,len(pa)*len(pb)]); count+=edges[-1][3]
s=json.loads((Q/'summary.json').read_text()); assert count==s['perceptual_candidates']
obj={'sha256_duplicate_groups':[{'sha256':h,'paths':p} for h,p in exact.items() if len(p)>1],'perceptual_method':'ImageHash 64-bit dHash; all image pairs Hamming <=4; uncalibrated screening only. Full-path pair list losslessly represented by hash buckets and bucket edges. Distinct buckets expand Cartesian product; same bucket expands unordered distinct path pairs. High collision rate suggests poor discrimination; do not equate with identity.','perceptual_candidate_pair_count':count,'dhash_buckets':dict(items),'perceptual_bucket_edges':edges,'edge_schema':['hash_a','hash_b','hamming_distance','represented_image_pair_count'],'unique_dhashes':len(items)}
with (Q/'duplicates.json').open('w',encoding='utf-8') as out: json.dump(obj,out,separators=(',',':'))
print({'pair_count':count,'buckets':len(items),'bucket_edges':len(edges),'bytes':(Q/'duplicates.json').stat().st_size})
