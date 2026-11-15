---
name: Kaggle
description: Run private Kaggle notebook jobs remotely through the official Kaggle CLI: prepare and upload notebooks, start and monitor GPU sessions, and retrieve model artifacts. Use for @kaggle or remote Kaggle training requests.
---

# Kaggle remote notebook training

Use this skill's `kaggle` launcher, which installs the official `kaggle` CLI into
its own namespaced Linux cache via UV when absent, authenticated with the user's API token/key. Do not
use browser/CDP automation, interactive sessions, UI clicks or local training.

## Setup

The user creates an API token at `https://www.kaggle.com/settings/api`. Authenticate
using one of the official CLI methods: `~/.agents/skills/kaggle/kaggle auth login`, `KAGGLE_API_TOKEN`,
`~/.agents/skills/kaggle/.kaggle/access_token`, or legacy
`~/.agents/skills/kaggle/.kaggle/kaggle.json`. Never print, commit,
copy into notebooks or expose credentials. If the `kaggle` CLI is absent, tell the
user; do not silently install it or use another transport.

## Procedure

1. Inspect the complete local notebook, adapt it for noninteractive execution and
   make model artifacts explicit files in `/kaggle/working`.
2. Create a fresh local upload directory containing exactly the `.ipynb` and
   `kernel-metadata.json`:

   ```json
   {
     "id": "elxecutor/your-notebook-slug",
     "title": "Your notebook title",
     "code_file": "notebook.ipynb",
     "language": "python",
     "kernel_type": "notebook",
     "is_private": "true",
     "enable_gpu": "true",
     "enable_internet": "false",
     "machine_shape": "NvidiaTeslaT4",
     "dataset_sources": [],
     "competition_sources": [],
     "kernel_sources": [],
     "model_sources": []
   }
   ```

   Add only approved Kaggle inputs. Set `enable_internet` only when the notebook
   genuinely needs network access. Preserve the original notebook and avoid stale
   execution outputs.
3. Submit the background GPU version once:

   ```bash
   ~/.agents/skills/kaggle/kaggle kernels push -p UPLOAD_DIR --accelerator NvidiaTeslaT4
   ```

   This creates/updates the private notebook and runs it remotely. It is not local
   execution or an interactive session. Do not use `--no-run` for training.
4. Monitor the exact handle; do not resubmit just because a command times out:

   ```bash
   ~/.agents/skills/kaggle/kaggle kernels status elxecutor/your-notebook-slug
   ~/.agents/skills/kaggle/kaggle kernels logs elxecutor/your-notebook-slug --follow --interval 10
   ```

   Wait for completion, inspect errors/logs, then list expected outputs:

   ```bash
   ~/.agents/skills/kaggle/kaggle kernels files elxecutor/your-notebook-slug
   ```
5. Download outputs to a new empty directory:

   ```bash
   ~/.agents/skills/kaggle/kaggle kernels output elxecutor/your-notebook-slug -p OUTPUT_DIR
   ```

   Use `--file-pattern` when only selected artifact names are wanted. Do not use
   `--force` unless the user explicitly authorized overwriting. Verify expected
   filenames, sizes and SHA-256 locally; never deserialize models merely to test
   them.

## Rules

- Prefer GPU. If GPU submission is rejected/unavailable, report it before choosing
  CPU; do not silently change the requested resource. The API requests hardware;
  quota, entitlement and server policy determine what is actually granted. CPU is not needed to stop a
  background run: Kaggle owns the job lifecycle.
- Ask before first remote submission/GPU use, publishing, deletion, overwriting,
  accepting competition rules, enabling internet, attaching private inputs or
  external uploads. A request to train described models authorizes that single
  private run plan after source inspection.
- Keep notebooks private by default. Use a new slug/private workspace rather than
  overwriting an existing notebook unless specifically approved.
- Existing direct commands support source pull (`kaggle kernels pull`) and kernel
  deletion (`kaggle kernels delete HANDLE --yes`), but deletion requires explicit
  approval. There is no need to start/stop an interactive worker for this flow.
- Report the notebook URL/handle, terminal status, requested accelerator, logs on
  failure and downloaded artifact paths/hashes. Never claim success from upload or
  queueing alone.
