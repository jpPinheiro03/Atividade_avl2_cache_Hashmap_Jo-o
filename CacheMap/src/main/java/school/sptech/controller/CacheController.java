package school.sptech.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import school.sptech.cache.ConteudoCache;
import school.sptech.service.ConteudoService;

@RestController
@RequestMapping("/cache")
public class CacheController {

    private final ConteudoService service;

    public CacheController(ConteudoService service) {
        this.service = service;
    }

    @GetMapping("/estatisticas")
    public ConteudoCache.Estatisticas estatisticas() {
        return service.estatisticas();
    }

    @DeleteMapping
    public ResponseEntity<Void> limpar() {
        service.limparCache();
        return ResponseEntity.noContent().build();
    }
}
