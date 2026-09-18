# PUBLICAR.md — checklist de publicación (para el autor; borrar al terminar)

Todo lo de acá lo ejecuta el autor: git, GitHub, licencias y el PDF. Nada lo hace un agente.

1. [x] **Licencias.** *(2026-09-18: aplicado. Paraguas **CC BY 4.0**, con el texto legal completo
       —8 secciones, 396 líneas—, así que la salvedad de la versión corta ya no aplica. Los cinco
       repos de código tienen **MIT** en su propio `LICENSE`, con el copyright a nombre de los tres
       autores del `CITATION.cff`. Dos repos llevan además una nota en su README porque la licencia
       propia no alcanza a todo lo que distribuyen: `e-ovrt_datasets`, donde cada conjunto de datos
       de terceros conserva la suya —registro en `datasets/registry/license_registry.md`—, y
       `e-ovrt_media-plane`, cuya dependencia de inferencia de YOLOE es **AGPL-3.0** y obliga a un
       despliegue derivado a publicar su código bajo la misma licencia o a licenciarla
       comercialmente.)*
       **Queda del autor confirmar la elección con los coautores**; los archivos ya están puestos
       y un cambio de licencia es un commit.
2. [ ] **Barrido de secretos** en la historia de los 5 repos antes de hacerlos públicos.
       Verificado el 2026-08-25: `cameras/` nunca fue commiteado; el `.env` histórico de
       `infra/platform` sólo contenía `EOVRT_WORKSPACE` y `COMPOSE_PROFILES`. Como constancia,
       correr en cada repo: `git log -p --all | grep -n -i -E 'password|api_key|secret|rtsp://[^*]' | head`
       (o `gitleaks detect` si está instalado).
3. [ ] **Coherencia de READMEs.** El primer párrafo del `README.md` de cada repo dice lo mismo
       que su ficha en `repositorios/README.md`.
4. [x] **Rama por defecto.** *(2026-09-18: RESUELTO. Los cinco repositorios de código tienen el
       trabajo integrado en `main` por fast-forward, y `main` es su rama por defecto en GitHub.
       `evidencia/mapa-de-artefactos.md` dejó de enlazar por nombre de rama y apunta a `main`.)*
       Los enlaces de este repo usan `blob/HEAD/` (= rama por defecto en GitHub), que ahora
       resuelve a `main` en todos. `e-ovrt_experimental-setup` contiene `results/` y
       `finetuning/manifests/` en `main`, tal como se enlazan.
5. [ ] **Crear el repo** `simonll4/e-ovrt-vdp` en GitHub, público. Descripción:
       *Plataforma experimental de detección open-vocabulary en video en tiempo real para
       monitoreo asistivo de riesgos en construcción — Proyecto Integrador, Ingeniería en
       Informática, IUA Córdoba (2026).* Topics: `open-vocabulary-detection`,
       `construction-safety`, `grounding-dino`, `computer-vision`, `thesis`, `zeromq`, `mqtt`.
       Luego: `git remote add origin git@github.com:simonll4/e-ovrt-vdp.git && git add -A &&
       git commit -m "Repositorio público e-ovrt-vdp" && git push -u origin main`.
6. [ ] **Hacer públicos** los 5 repos de código.
6b. [ ] **C1 — URLs de los clips de internet.** Los 13 `clip.yaml` del lote de internet tienen
        `license.video_url: TODO`; por eso `evidencia/material-de-video.md` muestra
        "*(sin URL registrada)*" en las 13 filas. Completar las URLs (y fecha de acceso) en los
        `clip.yaml` y volcarlas a la tabla de `material-de-video.md`.
7. [ ] **Informe.** Cuando cierre el maestro: exportar PDF → `informe/E-OVRT-VDP-informe.pdf`;
       actualizar versión, fecha y tabla de contenidos en `informe/README.md`.
8. [ ] **Congelar.** En cada repo de código: `git tag -a informe-2026 -m "Versión citada en el informe" <commit> && git push origin informe-2026`.
       Completar la tabla de versiones de `repositorios/README.md` (tag, commit corto, fecha).
       Opcional, para permanencia: `grep -rlE 'blob/HEAD/|tree/HEAD/' --include='*.md' . | xargs
       sed -i 's#\(blob\|tree\)/HEAD/#\1/informe-2026/#g'`
       y volver a correr `python3 herramientas/verificar.py`. En `CITATION.cff` ajustar
       `date-released` y `version`. Crear el Release `v1.0` con el PDF adjunto.
9. [ ] **Citar.** Poner `https://github.com/simonll4/e-ovrt-vdp` en la sección de entrega /
       anexos del informe.
10. [ ] Borrar este archivo y su mención en `CONTRIBUTING.md`.
