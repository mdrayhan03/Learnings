# DevOps Mastery Roadmap — Terraform, CI/CD & Kubernetes

> **For:** MD Rayhan Hossain — Full Stack Engineer → DevOps-capable engineer
> **Goal:** Go from "I use Docker & Azure" to "I treat infrastructure as software" — the exact phrase the SysModeler.ai role asked for.
> **How to use this:** Read a section → do the "Hands-On" → then apply it to **your own project** (TraderBro / CWTAMC / RideBuddy). Don't just read. The learning happens when you break something and fix it.

---

## 0. The Mental Model (read this first — it makes everything click)

These three tools are **not separate skills**. They're three stages of one pipeline. Understand how they connect and each one stops feeling random.

```
   YOU WRITE CODE                    THE PIPELINE                    THE RESULT
 ┌────────────────┐          ┌──────────────────────────┐      ┌─────────────────┐
 │  App code       │          │  CI/CD (GitHub Actions)  │      │  Kubernetes     │
 │  (Django/FastAPI)│  push → │  - build Docker image     │ →   │  runs your      │
 │                 │          │  - run tests              │      │  containers,    │
 │  Terraform code │          │  - push image to registry │      │  keeps them     │
 │  (.tf files)    │          │  - apply Terraform        │      │  alive & scaled │
 └────────────────┘          └──────────────────────────┘      └─────────────────┘
       ▲                                                                 │
       │                                                                 │
       └──── Terraform CREATED the Kubernetes cluster in the first place ┘
```

**One sentence each:**
- **Terraform** = writes down *what infrastructure should exist* (servers, clusters, databases, networks) as code, so you can create/destroy it reproducibly instead of clicking in the Azure portal.
- **CI/CD** = the robot that runs *every time you push code*: tests it, packages it, and ships it — so deploying isn't a manual, error-prone ritual.
- **Kubernetes** = the system that *runs your containers in production*: restarts them when they crash, scales them under load, and rolls out new versions without downtime.

**The "infrastructure as software" mindset** (the thing that separates junior from advanced): every part of your system — the server, the network, the deploy steps, the scaling rules — is written in a file, version-controlled in Git, reviewed in a PR, and reproducible. **No clicking. No "it works on my machine." No undocumented manual steps.** If your infra got deleted, you could rebuild it 100% from your Git repo.

---

## PART 1 — TERRAFORM (Infrastructure as Code)

### Why it exists
Right now you deploy CWTAMC by (probably) logging into Azure, creating resources by hand, configuring them, and remembering what you did. That's not reproducible and not reviewable. Terraform replaces all that clicking with `.tf` files. You run `terraform apply` and your entire cloud setup appears. Delete a file, apply again, it's gone. **That's the whole pitch: your cloud becomes code.**

### 1.1 Basics — the foundation

**Core concepts (learn these 5 words cold):**

| Term | What it means | Analogy |
|---|---|---|
| **Provider** | The plugin for a cloud (azurerm, aws, google) | The "driver" for Azure |
| **Resource** | One thing you create (a VM, a database, a container) | A single object |
| **State** | Terraform's record of what it has created (`terraform.tfstate`) | Its memory / source of truth |
| **Plan** | A preview of what will change before it happens | `git diff` for infrastructure |
| **Apply** | Actually make the changes real | `git push` for infrastructure |

**The core workflow (memorize this loop):**
```bash
terraform init      # download the provider plugins (run once per project)
terraform plan      # preview: "here's what I WILL change" — always read this
terraform apply     # do it for real (asks for confirmation)
terraform destroy   # tear it all down (great for saving money on test infra)
```

**Your first real file** — provisioning an Azure resource group + container instance (maps directly to CWTAMC):
```hcl
# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "cwtamc" {
  name     = "cwtamc-rg"
  location = "Southeast Asia"
}

resource "azurerm_container_group" "app" {
  name                = "cwtamc-backend"
  location            = azurerm_resource_group.cwtamc.location
  resource_group_name = azurerm_resource_group.cwtamc.name
  os_type             = "Linux"

  container {
    name   = "django-app"
    image  = "yourregistry.azurecr.io/cwtamc:latest"
    cpu    = "1"
    memory = "1.5"
    ports {
      port     = 8000
      protocol = "TCP"
    }
  }
}
```
Notice `azurerm_resource_group.cwtamc.name` — that's Terraform **referencing one resource from another**. This dependency graph is Terraform's superpower: it figures out creation order automatically.

**✅ Hands-On (Basics):** Install Terraform, run the file above against your Azure free tier. Run `plan`, read it, `apply`, see it in the portal, then `destroy`. You just made infrastructure appear and disappear from code.

### 1.2 Intermediate — writing it like a real engineer

- **Variables** — never hardcode. Put values in `variables.tf`:
  ```hcl
  variable "location" {
    type    = string
    default = "Southeast Asia"
  }
  # use as: location = var.location
  ```
- **Outputs** — expose values after apply (e.g. the public IP of your app):
  ```hcl
  output "app_ip" {
    value = azurerm_container_group.app.ip_address
  }
  ```
- **`.tfvars` files** — per-environment values (`dev.tfvars`, `prod.tfvars`). Same code, different inputs → dev and prod from one codebase.
- **State management — THE most important intermediate topic.** The `terraform.tfstate` file is Terraform's brain. If you lose it or two people edit it at once, you corrupt your infra. **Solution: remote state** — store it in Azure Blob Storage with locking:
  ```hcl
  terraform {
    backend "azurerm" {
      resource_group_name  = "tfstate-rg"
      storage_account_name = "tfstateXXXX"
      container_name       = "tfstate"
      key                  = "prod.terraform.tfstate"
    }
  }
  ```
  > 🎯 **Advanced-engineer signal:** Knowing *why* remote state + locking matters (team collaboration, avoiding corruption) is a common interview question. Most juniors don't know state exists.

### 1.3 Advanced — what "advanced engineer" actually means here

- **Modules** — reusable, parameterized infra components. Instead of copy-pasting your container setup for every project, you write a `module` once and call it with different inputs. This is the DRY principle applied to infrastructure.
  ```hcl
  module "backend_service" {
    source   = "./modules/container-app"
    app_name = "traderbro"
    image    = "traderbro:latest"
  }
  ```
- **Workspaces** — manage dev/staging/prod from the same code without duplication.
- **`count` and `for_each`** — create N copies of a resource programmatically (e.g. 3 identical worker containers).
- **Provisioners & lifecycle rules** — `create_before_destroy`, `prevent_destroy` (stops you from accidentally deleting prod).
- **Terraform + CI/CD together** — run `terraform plan` automatically on every PR and post the diff as a comment; run `apply` only after merge. This is the real-world professional workflow.
- **Drift detection** — knowing when someone changed infra manually in the portal (drift) and Terraform wants to revert it.
- **Secrets** — NEVER put passwords in `.tf` files. Use Azure Key Vault / environment variables / a secrets manager.

**🎓 You're "advanced" in Terraform when you can:** structure a multi-environment project with modules and remote state, explain the state-locking problem, and wire `plan`-on-PR into CI. That's genuinely mid-to-senior DevOps.

---

## PART 2 — CI/CD (Continuous Integration / Continuous Delivery)

### Why it exists
Every time you `git push`, a robot should: run your tests, and if they pass, build + ship your app. No manual `docker build`, no manual deploy, no "oops I forgot to run the tests." You already write Django/pytest tests (it's on your resume) — CI/CD is what makes them actually protect you automatically.

### 2.1 Basics

**Two halves:**
- **CI (Continuous Integration)** = on every push, automatically **build + test** the code. Catches bugs before merge.
- **CD (Continuous Delivery/Deployment)** = automatically **ship** the tested code to a registry / server / cluster.

**The anatomy of a GitHub Actions workflow** (`.github/workflows/ci.yml`):
```yaml
name: CI                          # workflow name
on:                               # WHEN does it run?
  push:
    branches: [main]
  pull_request:

jobs:
  test:                           # a job = a set of steps on one machine
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # get the code
      - uses: actions/setup-python@v5      # install Python
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest                        # run YOUR tests
```
That's a complete, real CI pipeline for a Django/FastAPI project. Every PR now runs your tests automatically.

**Key vocabulary:** `workflow` (the whole file) → `job` (runs on one runner) → `step` (one command or action) → `runner` (the machine it runs on) → `action` (a reusable pre-built step, like `checkout`).

**✅ Hands-On (Basics):** Add the YAML above to RideBuddy or TraderBro. Push a commit. Watch it run in the "Actions" tab. Break a test on purpose and watch it go red. You now have automated testing.

### 2.2 Intermediate — build & ship, not just test

**The full CI/CD pipeline for your stack** — test → build Docker image → push to registry → deploy:
```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: pytest

  build-and-push:
    needs: test                        # only runs if tests pass
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to Azure Container Registry
        uses: docker/login-action@v3
        with:
          registry: yourregistry.azurecr.io
          username: ${{ secrets.ACR_USERNAME }}   # secrets, not hardcoded
          password: ${{ secrets.ACR_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: yourregistry.azurecr.io/traderbro:${{ github.sha }}
```
Key ideas here:
- **`needs: test`** — jobs form a dependency chain. Don't ship broken code.
- **Secrets** — `${{ secrets.X }}` are encrypted values set in repo settings. **Never** hardcode credentials.
- **Image tagging with `github.sha`** — every build gets a unique, traceable tag tied to the exact commit. (Advanced tip: `:latest` is an anti-pattern in prod — you can't tell which version is running.)

### 2.3 Advanced

- **Matrix builds** — test against multiple Python versions / OSes in parallel automatically.
- **Caching** — cache `pip`/Docker layers so pipelines run in seconds, not minutes.
- **Environments & approvals** — require a manual "approve" before deploying to prod; auto-deploy to staging.
- **Deployment strategies** (huge for the "safety-critical systems" role):
  - **Rolling** — replace instances gradually (K8s default).
  - **Blue-Green** — run old + new side by side, flip traffic instantly, roll back instantly.
  - **Canary** — send 5% of traffic to the new version, watch metrics, then ramp up.
- **GitOps** — the advanced end-state: your Git repo is the single source of truth, and a tool (ArgoCD/Flux) automatically syncs the cluster to match Git. Deploy = merge a PR.
- **Security in CI** — scan images for vulnerabilities (Trivy), scan code (CodeQL), never leak secrets in logs.
- **`terraform apply` in CD** — infra changes ship through the same pipeline as code.

**🎓 You're "advanced" in CI/CD when you can:** design a multi-stage pipeline (test → build → scan → deploy to staging → approve → deploy to prod), explain rolling vs blue-green vs canary and *when to use each*, and use secrets/caching/matrix correctly.

---

## PART 3 — KUBERNETES (Container Orchestration)

### Why it exists
Docker runs *one* container on *one* machine. But in production you need: many containers, across many machines, that restart when they crash, scale when traffic spikes, and update with zero downtime. Doing that by hand is impossible. **Kubernetes (K8s) is the robot that manages your fleet of containers for you.** You declare "I want 3 copies of TraderBro always running" and K8s makes it true and *keeps* it true.

> ⚠️ **Honesty check:** K8s is the hardest of the three and the deepest rabbit hole. For the SysModeler role you need **solid basics + can-deploy-an-app**, not mastery. Learn 3.1 and 3.2 well; treat 3.3 as "know it exists."

### 3.1 Basics — the vocabulary and the mental model

**The mental model:** You describe the *desired state* ("3 replicas of my app, reachable on port 80"). K8s constantly works to make *reality* match that desired state. Container died? It starts a new one. This "desired state reconciliation" is the single most important K8s concept.

**Core objects (learn these 5):**

| Object | What it is |
|---|---|
| **Pod** | The smallest unit — usually one container (your Django app). Ephemeral, can die anytime. |
| **Deployment** | Manages Pods: "keep 3 replicas alive, here's how to update them." You almost always work with Deployments, not raw Pods. |
| **Service** | A stable network address for a set of Pods (Pods die & get new IPs; the Service IP stays constant). |
| **ConfigMap / Secret** | Configuration and credentials injected into Pods (your `DATABASE_URL`, API keys). |
| **Namespace** | A folder to isolate environments (dev/prod) in one cluster. |

**Your first manifests** — deploying TraderBro:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: traderbro
spec:
  replicas: 3                      # I want 3 copies always running
  selector:
    matchLabels: { app: traderbro }
  template:
    metadata:
      labels: { app: traderbro }
    spec:
      containers:
        - name: traderbro
          image: yourregistry.azurecr.io/traderbro:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef: { name: traderbro-secrets }   # inject env vars
---
# service.yaml — a stable address in front of the 3 pods
apiVersion: v1
kind: Service
metadata:
  name: traderbro-svc
spec:
  selector: { app: traderbro }
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer               # gives it an external IP
```

**The essential `kubectl` commands** (your daily driver):
```bash
kubectl apply -f deployment.yaml   # create/update from a file (declarative)
kubectl get pods                   # list running pods
kubectl get deployments            # list deployments
kubectl logs <pod-name>            # read a pod's logs (debugging!)
kubectl describe pod <pod-name>    # why is this pod not starting?
kubectl exec -it <pod> -- bash     # shell into a running container
kubectl delete -f deployment.yaml  # tear down
```

**✅ Hands-On (Basics):** Install `kind` or `minikube` (a local K8s cluster on your laptop — free). Apply the manifests above with a simple container. Run `kubectl get pods`, kill a pod with `kubectl delete pod X`, and watch K8s *automatically recreate it*. That "it came back by itself" moment is the whole point of K8s.

### 3.2 Intermediate

- **Health checks (probes)** — critical for "safety-critical systems":
  - **Liveness probe** — "is the app alive? if not, restart it."
  - **Readiness probe** — "is the app ready for traffic? if not, don't send any yet."
  ```yaml
  livenessProbe:
    httpGet: { path: /health, port: 8000 }
    initialDelaySeconds: 10
  ```
- **Resource requests & limits** — tell K8s how much CPU/memory each pod needs (prevents one runaway pod killing the node — you already monitor CPU/memory in Portainer, this is the K8s version).
- **Rolling updates & rollbacks** — `kubectl rollout status` / `kubectl rollout undo`. Update with zero downtime; instantly revert a bad deploy.
- **Ingress** — smart HTTP routing (path/host-based) in front of Services — one entry point, many apps.
- **Persistent Volumes** — how stateful things (databases) keep data when pods die.
- **AKS (Azure Kubernetes Service)** — the managed K8s on Azure you already use. Terraform can create the whole cluster (`azurerm_kubernetes_cluster`), closing the loop between all three tools.

### 3.3 Advanced (know it exists; go deep later)

- **Helm** — the "package manager" for K8s. Templatize your manifests into reusable charts. (Very commonly asked.)
- **Horizontal Pod Autoscaler (HPA)** — auto-scale replicas based on CPU/custom metrics. Real elasticity.
- **StatefulSets** — for databases and things needing stable identity/storage.
- **RBAC** — who can do what in the cluster (security).
- **Service mesh (Istio/Linkerd)** — advanced traffic management, mTLS, observability between services.
- **Operators & CRDs** — extend K8s with your own custom resource types.
- **Observability** — Prometheus (metrics) + Grafana (dashboards) + Loki (logs). The production-grade version of your current file-based logging.

**🎓 You're "advanced enough" for this job when you can:** write Deployment/Service/ConfigMap manifests from scratch, explain desired-state reconciliation, use probes and resource limits, do a rolling update + rollback, and deploy to AKS. Helm + HPA are a strong bonus.

---

## PART 4 — "What Infrastructure Should I Use?" (the decision framework you asked for)

You said you'll decide the infrastructure *after* thinking. Good instinct — **choosing the right complexity is itself a senior skill.** Don't use K8s because it's cool; use it because you need it. Here's how to actually decide.

### The complexity ladder — match the tool to the need

```
Simplicity ──────────────────────────────────────────────────► Power/Complexity

1. Single VM +        2. Azure Container      3. Managed platform    4. Kubernetes (AKS)
   Docker Compose        Instances (ACI)         (App Service /
                                                  Container Apps)
   ▲ You are here        ▲ Easy next step        ▲ Great middle       ▲ When you truly
     (CWTAMC today)        (little to learn)        ground               need orchestration
```

**Decision questions — answer honestly for each project:**

| Question | If "no" → stay simple | If "yes" → move up the ladder |
|---|---|---|
| Do I run **multiple services** that must scale independently? | Docker Compose is fine | Kubernetes earns its cost |
| Do I get **traffic spikes** needing auto-scaling? | A single sized VM is fine | HPA on K8s / Container Apps |
| Do I need **zero-downtime deploys** & self-healing? | Manual restart is acceptable | K8s gives it for free |
| Is my **team** able to operate K8s? | Don't adopt what you can't run | Worth it |
| Is it **safety-critical / high-availability**? | — | K8s / robust orchestration |

> 🧠 **The senior mindset:** "Kubernetes is a powerful tool AND a large operational burden. For a small app, it's over-engineering. For a multi-service, must-stay-up AI platform, it's the right call." Being able to say *when NOT to use K8s* impresses interviewers more than knowing every feature.

### My recommendation for YOUR projects (to practice on)

| Project | Realistic infra | Why | What it teaches you |
|---|---|---|---|
| **CWTAMC** (ERP, prod) | Terraform → **Azure Container Apps** or ACI | Real app, moderate needs, don't over-build | Terraform + CI/CD end-to-end |
| **TraderBro** (AI agent, multi-service) | Terraform → **AKS (Kubernetes)** | Genuinely multi-service (agent + caching + workers) → best K8s practice | All 3 tools together — your portfolio centerpiece |
| **RideBuddy** (student project) | **GitHub Actions CI** only | Just needs automated tests | CI/CD fundamentals cleanly |

**The portfolio play:** Do the **full stack of all three on TraderBro** — Terraform provisions an AKS cluster, GitHub Actions builds/tests/pushes the image, K8s runs it with probes and 3 replicas. That single repo demonstrates every must-have from the SysModeler.ai posting at once. It's the strongest possible artifact for that application.

---

## PART 5 — Suggested Learning Order & Timeline

Don't learn them in isolation — learn them in the order they *connect*.

**Week 1 — Docker refresh + CI/CD** *(fastest win, you're already close)*
1. Solidify Docker (multi-stage builds, `docker-compose`).
2. GitHub Actions: test workflow → full build-and-push workflow.
3. **Artifact:** RideBuddy or TraderBro with a green CI badge.

**Week 2 — Terraform** *(second win, high interview value)*
1. Basics: providers, resources, plan/apply on Azure.
2. Variables, outputs, remote state.
3. **Artifact:** CWTAMC's Azure infra as Terraform, in a public repo.

**Week 3–4 — Kubernetes** *(the deep one — pace yourself)*
1. Local cluster (kind/minikube) + core objects + `kubectl`.
2. Deployment/Service/ConfigMap for a real app + probes + rolling update.
3. Deploy to AKS (created by your Terraform).
4. **Artifact:** TraderBro running on AKS, the whole pipeline wired together.

**Then:** loop back and add the "advanced" items (Helm, HPA, canary deploys, monitoring) as you have time.

---

## The One Thing To Remember

> **Don't learn these as three trivia lists. Learn them as one story:** you write app code *and* infrastructure code → CI/CD tests and ships it → Kubernetes (that Terraform created) runs it, heals it, and scales it. Every concept above is a detail inside that one loop. If you can explain that loop *and show a repo where you built it*, you're not a junior who "knows Docker" anymore — you're the "backend engineer who treats infrastructure as software" that the job is looking for.

Build it once on TraderBro. That single repo is your resume, your interview story, and your proof — all at once.
