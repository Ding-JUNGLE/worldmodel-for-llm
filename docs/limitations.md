# Limitations

1. The memory module is external and inference-time only.
2. It does not modify Matrix-Game-2 internal attention.
3. It does not retrain the world model.
4. It does not use 3D geometry memory.
5. Candidate reranking requires multiple generations.
6. The current evidence is strongest as a qualitative road-sign case study.
7. A future version could add:
   - dynamic memory update
   - stronger feature encoders
   - internal reference-frame conditioning
   - 3D geometric memory
