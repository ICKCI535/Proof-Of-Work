from flask_restx import Model, fields


base_response_model = Model("BaseResponse", {
    "success": fields.Boolean()
})

operation_response_model = Model("OperationResponse", {
    "success": fields.Boolean(True)
})


error = Model("Error", {
    "type": fields.String(),
    "message":fields.String()
})

error_response_model = Model("ErrorResponse", {
    "success": fields.Boolean(True),
    "data":fields.List(fields.Nested(error))
})
