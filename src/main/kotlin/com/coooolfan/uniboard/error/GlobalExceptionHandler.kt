import cn.dev33.satoken.exception.NotLoginException
import jakarta.servlet.http.HttpServletRequest
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ProblemDetail
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler
import java.net.URI
// TODO 拦截不住
@RestControllerAdvice
class GlobalExceptionHandler : ResponseEntityExceptionHandler() {

    private val log = LoggerFactory.getLogger(GlobalExceptionHandler::class.java)

    @ExceptionHandler(NotLoginException::class)
    fun handleAccessDeniedException(
        ex: AccessDeniedException,
        request: HttpServletRequest
    ): ResponseEntity<Any> {
        log.error("权限不足: ", ex)

        val problemDetail = ProblemDetail.forStatusAndDetail(
            HttpStatus.FORBIDDEN,
            "当前用户没有权限执行此操作"
        )
        problemDetail.title = "权限不足"
        problemDetail.type = URI.create("https://api.yourservice.com/errors/forbidden")
        problemDetail.setProperty("timestamp", System.currentTimeMillis())
        problemDetail.setProperty("path", request.requestURI)

        return ResponseEntity.status(HttpStatus.FORBIDDEN)
            .body(problemDetail)
    }





}