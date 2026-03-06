(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  const elEmpresa = byId("id_empresa");
  const elData = byId("id_data");
  const elTelefone = byId("id_telefone");
  const elHorario = byId("id_horario");

  // 1) Flatpickr (DATA dd/mm/aaaa, sem datas passadas)
  if (elData && window.flatpickr) {
    flatpickr.localize(flatpickr.l10ns.pt);

    flatpickr(elData, {
      dateFormat: "d/m/Y",
      allowInput: true,
      minDate: "today",
      disableMobile: true,
    });
  }

  // 2) Máscara TELEFONE (00) 00000-0000
  if (elTelefone && window.IMask) {
    IMask(elTelefone, {
      mask: [
        { mask: "(00) 0000-0000" },   // 10 dígitos
        { mask: "(00) 00000-0000" },  // 11 dígitos
      ],
    });
  }

  // 3) Carregar HORÁRIOS por empresa (API) -> sempre HH:MM
  async function carregarHorarios() {
    if (!elEmpresa || !elHorario) return;

    const empresaId = elEmpresa.value;

    // limpa o select
    elHorario.innerHTML = "";
    const opt0 = document.createElement("option");
    opt0.value = "";
    opt0.textContent = empresaId ? "Carregando horários..." : "Selecione uma empresa primeiro";
    elHorario.appendChild(opt0);

    if (!empresaId) return;

    try {
      const resp = await fetch(`/api/horarios-por-empresa/?empresa_id=${encodeURIComponent(empresaId)}`);
      const data = await resp.json();

      elHorario.innerHTML = "";

      const opt1 = document.createElement("option");
      opt1.value = "";
      opt1.textContent = "Selecione um horário";
      elHorario.appendChild(opt1);

      (data.horarios || []).forEach((h) => {
        const opt = document.createElement("option");
        opt.value = h.id;

        // garante HH:MM mesmo se vier HH:MM:SS
        const txt = String(h.horario || "").trim().slice(0, 5);
        opt.textContent = txt;

        elHorario.appendChild(opt);
      });
    } catch (e) {
      elHorario.innerHTML = "";
      const optErr = document.createElement("option");
      optErr.value = "";
      optErr.textContent = "Erro ao carregar horários";
      elHorario.appendChild(optErr);
      console.error(e);
    }
  }

  if (elEmpresa) {
    elEmpresa.addEventListener("change", carregarHorarios);
    // carrega ao abrir a página (se já tiver empresa selecionada)
    carregarHorarios();
  }
})();