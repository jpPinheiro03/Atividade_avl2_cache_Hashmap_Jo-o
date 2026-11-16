package school.sptech.mapper;

import org.springframework.stereotype.Component;
import school.sptech.dto.ConteudoRequest;
import school.sptech.dto.ConteudoResponse;
import school.sptech.entity.Conteudo;

@Component
public class ConteudoMapper {

    public ConteudoResponse toResponse(Conteudo conteudo) {
        return new ConteudoResponse(
                conteudo.getId(),
                conteudo.getTitulo(),
                conteudo.getCorpo(),
                conteudo.getAutor(),
                conteudo.getAtualizadoEm());
    }

    public Conteudo toEntity(ConteudoRequest request) {
        return new Conteudo(request.titulo(), request.corpo(), request.autor());
    }
}
