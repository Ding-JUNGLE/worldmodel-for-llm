# Evidence Ladder

## Level 1: Pipeline Feasibility

Question:
Can we attach external memory to Matrix-Game-2?

Evidence:
Day1 external memory reranking passed.

Conclusion:
External memory can be written, read, and used for candidate selection.

## Level 2: Weak Memory Effectiveness

Question:
Does full-frame memory beat no-memory?

Evidence:
Windmill / universal-scene fallback showed full_memory beat no_memory and recent_only but tied random_memory.

Conclusion:
Generic memory is not specific enough.

## Level 3: Landmark Memory

Question:
Does landmark-specific memory change selection?

Evidence:
GTA landmark memory selected a different seed from no_memory and uniform_memory.

Conclusion:
Landmark memory creates a more specific selection signal.

## Level 4: Approved Road-Sign Memory

Question:
Can a human-approved object-level memory target change the final output?

Evidence:
No-memory selected seed1.
Approved road-sign memory selected seed8.

Conclusion:
Object-level external memory can guide candidate selection.

## Final claim

The evidence supports a case-study conclusion:

External object-level memory can influence generation selection in a frozen interactive world model.

It does not prove a universal solution to spatial forgetting.
