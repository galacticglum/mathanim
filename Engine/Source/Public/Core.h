#define BIT(x) 1 << x
#define BIND_EVENT(fn) std::bind(&fn, this, std::placeholders::_1) 