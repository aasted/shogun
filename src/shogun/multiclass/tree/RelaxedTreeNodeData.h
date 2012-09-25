/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * Written (W) 2012 Chiyuan Zhang
 * Copyright (C) 2012 Chiyuan Zhang
 */

#ifndef RELAXEDTREENODEDATA_H__
#define RELAXEDTREENODEDATA_H__

#include <shogun/base/SGObject.h>
#include <shogun/base/Parameter.h>
#include <shogun/lib/SGVector.h>

namespace shogun
{

/** Data for the tree nodes in a RelaxedTree */
class RelaxedTreeNodeData: public CSGObject
{
public:
    /** constructor */
    RelaxedTreeNodeData()
        :mu(NULL)
    {
        SG_ADD(&mu, "mu", "Vector of class labels", MS_NOT_AVAILABLE);
    }

	/** mu */
	SGVector<int32_t> mu;

	/** print data */
	static void print_data(const RelaxedTreeNodeData &data)
	{
		SG_SPRINT("left=(");
		for (int32_t i=0; i < data.mu.vlen; ++i)
			if (data.mu[i] == -1 || data.mu[i] == 0)
				SG_SPRINT("%4d", i);
		SG_SPRINT("), right=(");
		for (int32_t i=0; i < data.mu.vlen; ++i)
			if (data.mu[i] == 1 || data.mu[i] == 0)
				SG_SPRINT("%4d", i);
		SG_SPRINT(")\n");
	}

	/** print data to a file handle*/
    static void save_data(FILE* modelfl, const RelaxedTreeNodeData &data)
    {
        fprintf(modelfl, "left=(");
        for (int32_t i=0; i < data.mu.vlen; ++i)
        if (data.mu[i] == -1 || data.mu[i] == 0)
            fprintf(modelfl, "%4d", i);
        fprintf(modelfl, "), right=(");
        for (int32_t i=0; i < data.mu.vlen; ++i)
            if (data.mu[i] == 1 || data.mu[i] == 0)
                fprintf(modelfl, "%4d", i);
        fprintf(modelfl, ")\n");
    }
};

} /* shogun */ 

#endif /* end of include guard: RELAXEDTREENODEDATA_H__ */

