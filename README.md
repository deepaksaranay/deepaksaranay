# GitLab CI/CD Practice — Manual Approval & Rollback

Ek chhota repo jiska maqsad app banana nahi, **pipeline mechanics seekhna** hai.
Focus: approval gates, protected environments, deployment history, rollback.

---

## Setup (5 min)

```bash
git init
git add .
git commit -m "chore: ci/cd practice scaffold"
git branch -M main
git remote add origin git@gitlab.com:<username>/cicd-practice.git
git push -u origin main
```

Push karte hi pipeline chalu ho jayega: **Build → Test → Staging** automatic,
**Production** pe ruk jayega (blue play button dikhega).

---

## Pipeline map

| Stage | Job | Trigger | Kya sikhata hai |
|---|---|---|---|
| build | `build` | auto | artifacts, `expire_in` |
| test | `test` | auto | `needs:`, JUnit reports |
| staging | `deploy:staging` | auto (main only) | `environment:`, `rules:` |
| production | `deploy:production` | **manual** | approval gate, `resource_group` |
| production | `stop:production` | manual | `action: stop`, `on_stop` |
| rollback | `rollback:production` | **manual + variable** | emergency job, `needs: []` |

---

## Manual approval kaise kaam karta hai

```yaml
rules:
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    when: manual
    allow_failure: false
```

- `when: manual` → job apne aap nahi chalta, koi insaan play dabata hai.
- `allow_failure: false` → pipeline status **blocked** rehta hai jab tak approve na ho.
  (Agar `true` hota to pipeline "passed" dikh jaata bina deploy ke — classic trap.)
- Kaun approve kar sakta hai? Jiske paas branch/environment pe **Deploy permission** ho.

**Asli gate lagane ke liye ye zaroor karo (Free tier me bhi):**
- Settings → Repository → **Protected branches** → `main` (no force push)
- Settings → CI/CD → **Protected environments** → `production` → sirf Maintainers deploy kar sakein

> Multi-person approval rules (2 log approve karein tab deploy ho) GitLab **Premium** feature hai.
> Free tier pe `when: manual` + protected environment hi practical gate hai.

---

## Rollback ke 3 tareeke (teeno try karo)

**1. GitLab ka built-in re-deploy (sabse fast)**
Deployments → Environments → `production` → deployment history → purane deploy ke aage **Re-deploy** button.
Ye us purane commit ka `deploy:production` job dobara chalata hai. Zero YAML.

**2. Is repo ka `rollback:production` job**
CI/CD → Pipelines → pipeline kholo → `rollback:production` job pe **Run job** →
Variables me `ROLLBACK_TO` = purana short SHA daalo → Run.

**3. Git revert + forward fix (best practice)**
```bash
git revert <bad-commit-sha>
git push
```
Naya commit → naya pipeline → wahi approval gate. Audit trail saaf rehta hai.

> Rule of thumb: **incident ke waqt #1 ya #2, cool down ke baad #3.**

---

## Exercises — order me karo

1. Push karo, pipeline blocked dekho, production approve karo.
2. `deploy:production` me `allow_failure` ko `true` karo, push karo — dhyaan do pipeline **green** ho jaata hai bina deploy ke. Wapas `false` karo. *(Ye #1 real-world bug hai.)*
3. `scripts/test.sh` me ek check jaan bujh ke fail karao — dekho `deploy:staging` bhi nahi chala.
4. Do commits push karo, dono production pe deploy karo, phir `ROLLBACK_TO` se pehle wale pe wapas jao.
5. `production` ko protected environment banao, phir kisi non-maintainer se approve karwane ki koshish karo.
6. `resource_group: production` hata do, do pipelines ek saath prod pe bhejo — race dekho. Phir wapas lagao.
7. `stop:production` chalao, Environments page pe environment ka status badalte dekho.

---

## Debugging tips

- YAML galat hai? → CI/CD → Editor → **Validate** tab (push karne se pehle).
- Job kyun nahi chala? → Pipeline → job → **"Job is stuck"** ya rules mismatch. `rules:` top-se-bottom evaluate hota hai, **pehla match jeet jaata hai**.
- Artifact nahi mila? → downstream job me `needs:` ya `dependencies:` check karo.
- Runner nahi mil raha? → Settings → CI/CD → Runners → "Instance runners" enabled hona chahiye.
