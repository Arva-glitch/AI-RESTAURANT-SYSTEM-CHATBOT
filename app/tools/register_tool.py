# Register every tool in one place.

from app.tools.tool_registery import registry
from app.tools.booking_tool import BookingTool
from app.tools.menu_tool import MenuTool
from app.tools.order_tool import OrderTool
from app.tools.payment_tool import PaymentTool
from app.tools.faq_tool import FAQTool
from app.tools.recommendation_tool import RecommendationTool

registry.register(BookingTool())
registry.register(MenuTool())
registry.register(OrderTool())
registry.register(PaymentTool())
registry.register(FAQTool())
registry.register(RecommendationTool())

# main purpose is to execute the registrations and not return anything
