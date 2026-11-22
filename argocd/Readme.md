ADO Pipeline
  └── version.txt = "1.0.456" → GitHub push
                                      ↓ TRIGGER
                            GitHub Actions (3 Stages)
                              │
                              ├── Stage 1: Pulumi
                              │     ├── Cluster already hai? → Skip
                              │     └── Nahi hai? → pulumi up → GKE create
                              │
                              ├── Stage 2: Argo Install
                              │     ├── Already installed? → Skip
                              │     └── Nahi? → install + RBAC setup
                              │
                              └── Stage 3: Argo Submit
                                    ├── WorkflowTemplate apply
                                    └── argo submit (version=1.0.456)
                                              ↓
                                    Argo Workflows (GKE par)
                                      ├── Step 1: GitHub Release se ZIP download
                                      └── Step 2: Helm deploy
                                                image.tag=1.0.456 ✅
