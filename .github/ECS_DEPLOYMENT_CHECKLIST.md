# ECS deployment checklist (Week 3)

Use this checklist to finish setting up GitHub Actions and get a successful deployment to ECS.

---

## 1. Set up GitHub Actions

Do this first so workflows can run.

1. **Enable Actions for the repository**
   - On GitHub: open your repo → **Settings** → **Actions** → **General**.
   - Under "Actions permissions", choose **Allow all actions and reusable workflows** (or your org’s allowed set).
   - Under "Workflow permissions", choose **Read and write permissions** so the workflow can use the GITHUB_TOKEN as needed (e.g. for deployment).
   - Click **Save** if you changed anything.

2. **Ensure the workflow file is in the repo**
   - The workflow must live at `.github/workflows/aws.yml` in the default branch (e.g. `main`).
   - If you cloned the bootcamp repo, it’s already there. After you push or merge to `main`, GitHub will pick it up automatically.
   - To confirm: repo → **Actions** tab. You should see a workflow named **"Deploy to Amazon ECS"**.

3. **Optional: Create the environment used by the workflow**
   - Repo → **Settings** → **Environments** → **New environment**.
   - Name it **`development`** (the workflow uses `environment: development`).
   - Save. You can add protection rules or secrets later if you want.

---

## 2. Repo: Task definition (your AWS account)

- Edit **`.github/workflows/task_definition.json`**.
- Replace the AWS account ID `798223350085` with **your** account ID.
- Replace task family, role ARNs, and any other names if your ECS cluster, service, or IAM roles use different names.

---

## 3. Repo: Workflow env vars

- Edit **`.github/workflows/aws.yml`** and check the `env:` block at the top:
  - **`AWS_REGION`** – e.g. `us-west-1` (same region as your ECR and ECS).
  - **`ECR_REPOSITORY`** – e.g. `iris_pred`.
  - **`ECS_SERVICE`** – your ECS service name (e.g. `iris_pred`).
  - **`ECS_CLUSTER`** – your ECS cluster name (e.g. `MLOpsCampDev`).
  - **`CONTAINER_NAME`** – must be **`iris_pred`** (must match the container name in the task definition).

---

## 4. GitHub: Actions secrets

- Repo → **Settings** → **Secrets and variables** → **Actions**.
- **New repository secret** (or add to the `development` environment if you use it):
  - **`AWS_ACCESS_KEY_ID`** – IAM user access key with ECR + ECS permissions.
  - **`AWS_SECRET_ACCESS_KEY`** – secret key for that IAM user.

The IAM user needs (at least) permissions to push images to ECR and to update ECS services/task definitions. See [GitHub: Deploying to Amazon ECS](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service) for suggested policies.

---

## 5. AWS: ECR, ECS, IAM

- **ECR**: Create a repository (e.g. `iris_pred`) in the same region as in the workflow.
- **ECS**: Create cluster, service, and a Fargate task definition with container name **`iris_pred`** and port **8000**.
- **IAM**: Execution role and task role for ECS; IAM user for GitHub with ECR + ECS access (used in the secrets above).

---

## 6. Trigger a deployment

- Push or merge to **`main`**.
- Repo → **Actions** → open the latest **"Deploy to Amazon ECS"** run and confirm all steps succeed.

---

## Short checklist

| # | Where        | Task |
|---|--------------|------|
| 1 | **GitHub**   | **Set up GitHub Actions**: enable Actions (Settings → Actions → General), ensure `.github/workflows/aws.yml` is on `main`, optionally create environment `development`. |
| 2 | Repo         | Update `.github/workflows/task_definition.json` with your AWS account ID and resource names. |
| 3 | Repo         | Set `AWS_REGION`, `ECR_REPOSITORY`, `ECS_SERVICE`, `ECS_CLUSTER` (and `CONTAINER_NAME: iris_pred`) in `.github/workflows/aws.yml`. |
| 4 | **GitHub**   | Add **Actions secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`. |
| 5 | AWS          | Create ECR repo, ECS cluster/service/task definition, and IAM user/roles. |
| 6 | **GitHub**   | Push/merge to `main` and verify the workflow run in the Actions tab. |
