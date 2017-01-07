#ifndef PY2CPP_RANGE_HPP_
#define PY2CPP_RANGE_HPP_

#include <boost/range/irange.hpp>

namespace py2cpp {

    template<typename... Args>
    inline auto range(Args&&... args) -> decltype(boost::irange(std::forward<Args>(args)...))
    {
        return boost::irange(std::forward<Args>(args)...);
    }

    inline auto range(int last) -> decltype(range(0, last))
    {
        return range(0, last);
    }

} // py2cpp

#endif // PY2CPP_RANGE_HPP_
