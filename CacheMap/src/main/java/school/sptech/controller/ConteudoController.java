package school.sptech.controller;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import school.sptech.cache.ConteudoCache;
import school.sptech.dto.ConteudoRequest;
import school.sptech.dto.ConteudoResponse;
import school.sptech.entity.Conteudo;
import school.sptech.mapper.ConteudoMapper;
import school.sptech.service.ConteudoService;

@RestController
@RequestMapping("/conteudos")
public class ConteudoController {

    private final ConteudoService service;
    private final ConteudoMapper mapper;

    public ConteudoController(ConteudoService service, ConteudoMapper mapper) {
        this.service = service;
        this.mapper = mapper;
    }

    @GetMapping("/{id}")
    public ResponseEntity<ConteudoResponse> buscar(@PathVariable Long id) {
        ConteudoCache.Resultado<Conteudo> resultado = service.buscarPorId(id);
        if (resultado.valor() == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok()
                .header("X-Cache", resultado.hit() ? "HIT" : "MISS")
                .body(mapper.toResponse(resultado.valor()));
    }

    @PostMapping
    public ResponseEntity<ConteudoResponse> criar(@Valid @RequestBody ConteudoRequest request) {
        Conteudo salvo = service.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(mapper.toResponse(salvo));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ConteudoResponse> atualizar(@PathVariable Long id,
                                                      @Valid @RequestBody ConteudoRequest request) {
        Conteudo atualizado = service.atualizar(id, request);
        return ResponseEntity.ok(mapper.toResponse(atualizado));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> excluir(@PathVariable Long id) {
        service.excluir(id);
        return ResponseEntity.noContent().build();
    }
}
