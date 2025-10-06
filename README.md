# luit-aug-2025-python
Demo respository
Test Rekognition pipeline run <09132025>
git switch -c docs/readme-update
Add-Content README.md "`n- Fixed page rendering by converting Markdown `-` bullets to HTML <ul>/<li> in resume.md.`n- Used a feature branch (`feat/resume-format`); PR → beta deploy, merge to main → prod deploy.`n- Verified S3 pages and DynamoDB tracking; no manual console edits (IaC + CI/CD only).`n- Deleted the feature branch after merge to keep the repo clean."
git add README.md
git commit -m "Docs: add short summary of rendering fix & deploy flow"
git push -u origin docs/readme-update

flowchart LR
  Dev[Developer edits<br/>resume.md] --> PR[Pull Request]
  PR -->|CI: beta| GA[GitHub Actions]
  GA --> CFN[CloudFormation<br/>(idempotent)]
  GA --> PY[pipeline.py<br/>AI convert + ATS]
  PY --> S3[S3 bucket<br/>beta/ and prod/]
  PY --> DDB1[(DynamoDB<br/>ResumeAnalytics)]
  PY --> DDB2[(DynamoDB<br/>DeploymentTracking)]


```md
### CI/CD Flow
```mermaid
sequenceDiagram
  participant Dev as Developer
  participant GH as GitHub Actions
  participant CF as CloudFormation
  participant S3 as S3 (beta/prod)
  participant D1 as DDB: DeploymentTracking
  participant D2 as DDB: ResumeAnalytics

  Dev->>GH: Open PR
  GH->>CF: Deploy/Update stack
  GH->>GH: Run pipeline.py --env beta
  GH->>S3: Put beta/index.html
  GH->>D2: Put ATS analysis
  GH->>D1: Put deployment record (beta)

  Dev->>GH: Merge PR → main
  GH->>GH: Run pipeline.py --env prod
  GH->>S3: Copy beta/index.html → prod/index.html
  GH->>D1: Write deployment record (prod)


2) **Add a simple “Evidence” section with links** (no pics):
```md
### Evidence (links)
- Beta: https://testing-s3-bucket-access123.s3.us-east-1.amazonaws.com/beta/index.html
- Prod: https://testing-s3-bucket-access123.s3.us-east-1.amazonaws.com/prod/index.html
- Actions: link to your latest PR run and Merge-to-main run
- DynamoDB: tables `resume-site-DeploymentTracking` and `resume-site-ResumeAnalytics` contain items for the latest commit
